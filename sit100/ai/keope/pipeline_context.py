"""
pipeline_context.py
La classe PipelineContext gestisce ogni step della pipeline e si occupa di aggiornare la KeopeBank del progetto.
I dati sono salvati nella tabella Project tramite il campo keopebank, che è un campo JSON.
"""
from django.utils import timezone
from .cashflow_calculator import CashflowCalculator
from .photovoltaic_sizing import PhotovoltaicSizing
from .pvgis_client import PVGISClient
from .solar_calculator import SolarCalculator
from .keopebank import KeopeBank
from apps.project.models import Project
from .user_input_processor import UserInputProcessor
from .wordprojectconverter import ConverterProjectInWord
from .worddesignconverter import ConverterDesignInWord
from .xml_formatter import XMLFormatter
from .xml_compiler import XMLCompiler
from .xml_validator import XMLValidator


class PipelineContext:
    def __init__(self, project_code):
        self.project_code = project_code
        self.project = None
        self.keopebank = None
        self.project = None

    def initialize(self):
        # In ambiente reale recuperiamo il modello dal database
        self.project = Project.objects.get(project_code=self.project_code)
        if self.project.keopebank:
            self.keopebank = KeopeBank.from_dict(self.project.keopebank)
        else:
            self.keopebank = KeopeBank()

        # Debug: verifica lo stato iniziale del KeopeBank
        # data = self.keopebank.get_all_data()

    def save(self):
        try:
            # Converti il dizionario e decodifica i bytes
            kb_save = self.keopebank.to_dict()

            # Funzione per convertire bytes in stringa
            def convert_bytes_to_string(data):
                if isinstance(data, bytes):
                    return data.decode('utf-8')
                elif isinstance(data, dict):
                    return {key: convert_bytes_to_string(value) for key, value in data.items()}
                elif isinstance(data, list):
                    return [convert_bytes_to_string(item) for item in data]
                return data

            # Converti tutti i bytes in stringhe
            kb_save = convert_bytes_to_string(kb_save)

            # Aggiungi il timestamp
            kb_save['_last_update'] = timezone.now().isoformat()

            # Salva nel database
            Project.objects.filter(
                project_code=self.project_code).update(keopebank=kb_save)
            return True

        except Exception as e:
            print(f'Errore durante il salvataggio: {str(e)}')
            return False

    def add_data(self, data):
        self.keopebank.add_data(data)

    def get_data(self):
        return self.keopebank.get_all_data()

    def get_result(self):
        return self.keopebank.get_all_keopebank()
        # Restituisce il databank formattato come JSON
        # return json.dumps(self.keopebank, indent=4)

    def add_string_placeholders(self, data):
        self.keopebank.add_string_placeholders(data)

    def add_xml_placeholders(self, data):
        self.keopebank.add_xml_placeholders(data)

    def set_string_placeholder(self, key, value):
        self.keopebank.add_string_placeholder(key, value)

    def set_xml_placeholder(self, key, value):
        self.keopebank.add_xml_placeholder(key, value)

    def get_string_placeholders(self):
        return self.keopebank.get_string_placeholders()

    def get_xml_placeholders(self):
        return self.keopebank.get_xml_placeholders()

    def set_xml_data(self, key, value):
        self.keopebank.set_xml_data(key, value)

    def get_xml_data(self, key):
        return self.keopebank.get_xml_data(key)

    @staticmethod
    def read_xml_from_file(file_path):
        """Legge un file XML e restituisce il contenuto come stringa."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def save_xml_to_file(xml_string, file_path):
        """Salva una stringa XML in un file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(xml_string)

    # ---------------------------------------------------- STEP: Preparazione dei dati

    def user_input_preparation(self, data):
        """Primo step di keope: preparazione dei dati."""

        if not isinstance(data, dict):
            print("Data Non è un dizionario")
            return False

        processor = UserInputProcessor(data)
        result = processor.process_input_data()
        if result:
            self.add_data(result)  # Salva il risultato in keopebank
            self.save()  # salva i dati a fine step

            return True
        else:
            return False

    # ---------------------------------------------------- STEP: Calcolatore solare
    def solar_calculator(self):
        """Step: lancia le pipeline Sole10349, Perdite ed Energia."""
        data = self.get_data()
        calculator = SolarCalculator(data)
        ao1 = calculator.process_pipelines()
        if ao1:
            self.add_data(ao1)      # Salva il risultato in keopebank
            self.save()             # salva i dati a fine step
            return True
        else:
            return False

    # ---------------------------------------------------- STEP: Dimensionamento
    def pv_sizing(self):
        """Step: lancia la pipeline del dimensionamento."""

        photovoltaic_sizing = PhotovoltaicSizing(self.get_data())
        sizing = photovoltaic_sizing.process_pipelines()

        if sizing:
            self.add_data(sizing)      # Salva il risultato in keopebank
            self.save()                # salva i dati a fine step
            return True
        else:
            return False

    # ---------------------------------------------------- STEP: PVGIS

    def api_pvgis(self):
        """Step: gestisce la richiesta PVGIS tramite API."""

        pvgis = PVGISClient(self.get_data())
        data = pvgis.get_solar_data()
        if data:
            # Salva il risultato in keopebank
            self.add_data(data)
            self.save()                             # salva i dati a fine step
            return True
        else:
            return False

    # ---------------------------------------------------- STEP: Analisi economica finanziaria     TODO: da integrare
    def cashflow_calculator(self):
        """Step: lancia le pipeline Cashflow."""

        calculator = CashflowCalculator(self.get_data())
        output = calculator.process_pipeline()
        if output:
            # Salva il risultato in keopebank
            self.add_data(output)
            self.save()                             # salva i dati a fine step
            return True
        else:
            return False

    # ---------------------------------------------------- STEP: Generazione Grafici

    def graphs_generator(self):
        """Step: genera i grafici che si troveranno nel nostro progetto."""
        from .graphs_generator import GraphsGenerator

        generator = GraphsGenerator(self.get_data())
        graphs_data = generator.generate_all_graphs()

        if graphs_data:
            # Salva i dati dei grafici nel keopebank
            self.add_data(graphs_data)

            # Crea i placeholder XML per i grafici
            graph_placeholders = generator.create_graph_placeholders()
            if graph_placeholders:
                self.add_xml_placeholders(graph_placeholders)

            self.save()  # salva i dati a fine step
            return True
        else:
            return False
    # ---------------------------------------------------- STEP: Formattatore XML

    def xml_formatter(self):
        """Step: formattazione dei dati in nodi xml (stringa) per essere salvati in db."""

        formatter = XMLFormatter(self.get_data())
        string_placeholders, xml_placeholders = formatter.generate_placeholders_content()
        if string_placeholders and xml_placeholders:
            self.add_string_placeholders(string_placeholders)
            self.add_xml_placeholders(xml_placeholders)
            self.save()
            return True
        else:
            return False

    # ---------------------------------------------------- STEP: Compilazione XML

    def xml_compiler(self):
        """Recupera il template T3 coerente con il progetto e lo compila"""

        compiler = XMLCompiler(self.get_data(), self.get_string_placeholders(), self.get_xml_placeholders())

        # Template xml per il progetto
        t4_xml_string = compiler.create_final_project_xml_string()
        # Template xml per la distinta base di configurazione
        design_xml_string = compiler.create_final_design_xml_string()

        if t4_xml_string and design_xml_string:
            self.set_xml_data('t4_xml_string', t4_xml_string)
            self.set_xml_data('design_xml_string', design_xml_string)
            self.save()
            return True
        else:
            return False

    # ---------------------------------------------------- STEP: Validator XML

    def xml_validator(self):
        """Valida il t4 e lo trasforma in t5."""

        t4_xml_string = self.get_xml_data('t4_xml_string')
        if t4_xml_string is None:
            print("Non esiste la chiave 't4_xml_string' in xml_data")
            print("Verificare che xml_compiler() sia stato chiamato prima di xml_validator()")
            return False

        validator = XMLValidator(t4_xml_string)
        t5_xml_string = validator.convalide()

        if t5_xml_string:
            # Salva il risultato in keopebank
            self.set_xml_data('t5_xml_string', t5_xml_string)
            self.save()  # salva databank in db
            return True
        else:
            return False

    # ---------------------------------------------------- STEP: Converter docx

    def xml_converter_in_word_and_save(self):
        """Converte in xml in formato string in word."""

        # --- PROGETTO
        t5_xml_string = self.get_xml_data('t5_xml_string')
        if t5_xml_string is None:
            print("Non esiste la chiave 't5_xml_string' in xml_data")
            return False

        # Path di destinazione del progetto in word
        word_dest_path = self.get_data().get('word_project_path')
        if not word_dest_path:
            return False

        # --- DISTINTA BASE
        design_xml_string = self.get_xml_data('design_xml_string')
        if design_xml_string is None:
            print("Non esiste la chiave 'design_xml_string' in xml_data")
            return False

        # Path di destinazione della distinta base in word
        design_dest_path = self.get_data().get('word_design_path')
        if not design_dest_path:
            return False

        # --- CONVERSIONI IN WORD

        converter_project = ConverterProjectInWord(t5_xml_string, word_dest_path)
        is_project_word = converter_project.create_and_save_word()

        converter_design = ConverterDesignInWord(design_xml_string, design_dest_path)
        is_design_word = converter_design.create_and_save_word()

        if is_project_word and is_design_word:
            # salvare il path finale del word (es. media/project_files/1024/Report_1024.docx) in database Project
            filename_word = self.get_data().get('word_project_path', '')
            self.project.word_file = filename_word
            self.project.save()
            return True
        else:
            return False
