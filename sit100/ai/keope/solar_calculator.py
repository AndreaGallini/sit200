"""
solar_calculator.py
Classe che si occupa di lanciare le pipelines Sole10349, Losses ed Energy.
Ritorna il dizionario dei modelli.
"""
import re

from ..ao1.databank import DataBank
from ..ao1.pipelineenergy import PipelineEnergy
from ..ao1.pipelinesole10349 import PipelineSole10349
from ..ao1.pipelinelosses import PipelineLosses


class SolarCalculator:

    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_pipelines():
        return {
            "SOLE10349": {
                "MonthlyAvgDailyTemperature": "ARANCIONE SOLE 1",
                "AnnualAvgTemperature": "",
                "MonthlyAvgHorizontalIrradianceUni10349": "",
                "MonthlyAvgDailyArrayIrradianceUni10349": "",
                "MonthlyAvgDailyArrayIrradianceClassification": "",
                "MonthlyPlaneOfArrayIrradiance": "",
                "AnnualSolarRadiation": "",
                "TheoreticalAnnualYield": "",
                "MonthlyAvgDaylightHours": "",
                "AnnualAvgDaylightHours": "",
                "MonthlyAvgDailyHorizontalSolarIrradianceSummary": ""
            },
            "LOSSES": {
                "FixedSysMonthlyTempLoss": "",
                "FixedSysMonthlyEmpiricalTempLoss": "",
                "FixedSysMonthlyReflectionLoss": "",
                "FixedSysMonthlySoilingLoss": "",
                "FixedSysMonthlyLowIrradianceLoss": "",
                "FixedSysMonthlyMismatchingLoss": "",
                "FixedSysMonthlyCableLoss": "",
                "FixedSysMonthlyInverterLoss": "",
                "FixedSysMonthlyOtherLoss": "",
                "FixedSysMonthlyObstacleShading": "",
                "FixedSysMonthlyClinometricShading": "",
                "FixedSysMonthlyShadingLossPercentage": "",
                "FixedSysMonthlyShadingLoss": "",
                "FixedSysAnnualShadingLoss": "",
                "MonthlySystemLossesSummary": "",
                "MonthlySystemEfficiencySummary": ""
            },
            "ENERGY": {
                "MonthlyNetEnergy": "",
                "AnnualNetEnergy": "",
                "MonthlyEfficiencyPercentage": "",
                "MonthlyEnergyYield": "",
                "AnnualEnergyYield": "",
                "SystemEfficiency": "",
                "DailyAvgEnergyYield": "",
                "DailyEnergyYield": "",
                "MonthlyAvgEnergyProduction": "",
                "AnnualEnergyProduction": "",
                "AnnualLossPercentage": "",
                "AnnualLossPercentageClassification": "",
                "AnnualNetEnergyClassification": "",
                "SystemEfficiencyClassification": "",
                "GreenHouseGasesReduction": "",
                "TEPReduction": ""
            }
        }

    def run_pipeline(self, pipeline_name: str, the_db: DataBank):
        pipeline_processes = {
            "SOLE10349": PipelineSole10349(the_db),
            "LOSSES": PipelineLosses(the_db),
            "ENERGY": PipelineEnergy(the_db)
        }
        if pipeline_name not in pipeline_processes:
            return False
        pipeline = pipeline_processes[pipeline_name]
        if pipeline.run():
            return True
        else:
            return False

    def camel2snake(self, the_camel: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', the_camel).lower()

    def run_pipelines(self, the_db: DataBank):
        pipelines = self.get_pipelines()
        ao1 = {}
        for pipeline_name, pipeline_models in pipelines.items():
            if self.run_pipeline(pipeline_name, the_db):
                for model_name in pipelines[pipeline_name].keys():
                    model_output = the_db.get_model_output(model_name, True)
                    model_type = the_db.get_model_type(model_name)
                    # print(f"\n\n{model_name} ({model_type}):\n")
                    # print(model_output)
                    if model_type == 'single_valued':
                        ao1.update(model_output)
                    else:
                        model_key = self.camel2snake(model_name)
                        ao1.update({model_key: model_output})
                    # print("\n")
            else:
                # logger("ERROR", f"Uh! Oh! Something went wrong while running the pipeline: {pipeline_name}!")
                return {}
        return ao1

    @staticmethod
    def get_ceil_value(valore):
        """Arrotonda all'eccesso un numero secondo dei criteri definiti."""

        valore = int(valore)
        if valore < 1000:
            return (valore // 50 + 1) * 50
        elif valore < 10000:
            return (valore // 100 + 1) * 100
        else:
            return (valore // 500 + 1) * 500

    def get_max_for_chart(self, data):
        """Trova il valore massimo dei dati strutturati come da ao1 e calcola l'arrotondamento max,utile al grafico."""

        max_month, (max_value, max_um) = max(
            data.items(), key=lambda item: item[1][0])
        if max_value > 0:
            return self.get_ceil_value(max_value)
        else:
            return 0

    def get_max_irradiancy_energy(self, ao1_subfields):
        """
        Calcola la totale energia annua irraggiata sul piano dei moduli
        sommando i valori di tutti i sottocampi.

        Returns:
            float: Energia totale irraggiata annua in kWh/m²/anno
        """

        if not ao1_subfields:
            print("Nessun dato dei sottocampi disponibile")
            return 0.0

        total_annual_irradiance = 0.0

        for subfield_name, subfield_data in ao1_subfields.items():
            # Estrai il valore di radiazione solare annua per questo sottocampo
            annual_solar_radiation = subfield_data.get(
                'annual_solar_radiation')

            if annual_solar_radiation:
                # Se annual_solar_radiation è una tupla (valore, unità), prendi il valore
                if isinstance(annual_solar_radiation, (list, tuple)) and len(annual_solar_radiation) >= 2:
                    irradiance_value = annual_solar_radiation[0]
                    unit = annual_solar_radiation[1]
                else:
                    # Se è un valore diretto
                    irradiance_value = annual_solar_radiation
                # Somma il valore al totale
                try:
                    total_annual_irradiance += float(irradiance_value)
                except (ValueError, TypeError):
                    print(
                        f"Errore nella conversione del valore per {subfield_name}: {irradiance_value}")
                    continue
            else:
                print(
                    f"Nessun dato di radiazione solare annua per {subfield_name}")

        return total_annual_irradiance

    def get_total_net_energy(self, ao1_subfields):
        """
        Calcola la total_net_energy sommando i valori di annual_net_energy
        di tutti i sottocampi e li salva nel dizionario dei risultati.

        Returns:
            dict: Dizionario con total_annual_net_energy e total_monthly_net_energy
        """

        if not ao1_subfields:
            print("Nessun dato dei sottocampi disponibile per calcolare total_net_energy")
            return {
                'total_annual_net_energy': 0.0,
                'total_monthly_net_energy': {}
            }

        total_annual_net_energy = 0.0
        total_monthly_net_energy = {}

        # Inizializza i totali mensili
        months = ['GEN', 'FEB', 'MAR', 'APR', 'MAG', 'GIU', 'LUG', 'AGO', 'SET', 'OTT', 'NOV', 'DIC']
        for month in months:
            total_monthly_net_energy[month] = 0.0

        # Somma i valori di tutti i sottocampi
        for subfield_name, subfield_data in ao1_subfields.items():
            # Somma l'energia netta annua
            annual_net_energy = subfield_data.get('annual_net_energy')
            if annual_net_energy:
                if isinstance(annual_net_energy, (list, tuple)) and len(annual_net_energy) >= 2:
                    energy_value = annual_net_energy[0]
                    unit = annual_net_energy[1]
                else:
                    energy_value = annual_net_energy

                try:
                    total_annual_net_energy += float(energy_value)
                except (ValueError, TypeError):
                    print(
                        f"Errore nella conversione del valore annuo per {subfield_name}: {energy_value}")
                    continue

            # Somma l'energia netta mensile
            monthly_net_energy = subfield_data.get('monthly_net_energy', {})
            for month in months:
                if month in monthly_net_energy:
                    monthly_value = monthly_net_energy[month]
                    if isinstance(monthly_value, (list, tuple)) and len(monthly_value) >= 2:
                        value = monthly_value[0]
                        unit = monthly_value[1]
                    else:
                        value = monthly_value

                    try:
                        total_monthly_net_energy[month] += float(value)
                    except (ValueError, TypeError):
                        print(
                            f"Errore nella conversione del valore mensile per {subfield_name}, {month}: {value}")
                        continue

        # Risultati finali
        result = {
            'total_annual_net_energy': round(total_annual_net_energy, 2),
            'total_monthly_net_energy': {month: round(value, 2) for month, value in total_monthly_net_energy.items()}
        }
        return result

    def get_total_energy_production(self, ao1_subfields):
        total_energy = 0
        for subfield_name, subfield_data in ao1_subfields.items():
            total_energy += subfield_data.get('annual_energy_production', [])[0]
        total_energy = int(round(total_energy, 0))
        return total_energy

    def get_total_emission_reduction(self, ao1_subfields):
        ghg_reduction = 0
        tep_reduction = 0
        for subfield_data in ao1_subfields.values():
            ghg_list = subfield_data.get('green_house_gases_reduction', {}).get('ghg_co2_eq_reduction_total_tons', [])
            tep_list = subfield_data.get('t_e_p_reduction', {}).get('tep_reduction', [])
            if ghg_list:
                ghg_reduction += ghg_list[0]
            if tep_list:
                tep_reduction += tep_list[0]
        return round(ghg_reduction, 2), round(tep_reduction, 0)

    def str_range_subfield_solar_data(self, ao1_subfields):
        """Calcola i range dei valori solari tra i sottocampi."""

        def extract_value(field):
            """Estrae il primo elemento da una tupla/lista (valore, unità)."""
            if isinstance(field, (list, tuple)) and field:
                return field[0]
            return None

        def format_range(values, unit="", digits=0):
            values = [v for v in values if v is not None]
            if not values:
                return ""
            min_val = min(values)
            max_val = max(values)
            if min_val == max_val:
                return f"{min_val:.{digits}f}{unit}"
            else:
                return f"{min_val:.{digits}f} - {max_val:.{digits}f}{unit}"

        # Raccolta dati
        module_solar_radiation = []
        specific_producibility = []
        net_energy = []
        system_efficiency = []
        losses_percentage = []

        for subfield_data in ao1_subfields.values():
            module_solar_radiation.append(extract_value(subfield_data.get('annual_solar_radiation')))
            specific_producibility.append(extract_value(subfield_data.get('annual_energy_yield')))
            net_energy.append(extract_value(subfield_data.get('annual_net_energy')))
            system_efficiency.append(extract_value(subfield_data.get('system_efficiency')))
            losses_percentage.append(extract_value(subfield_data.get('annual_loss_percentage')))

        return {
            'module_solar_radiation': format_range(module_solar_radiation, " kWh/m²"),
            'specific_producibility': format_range(specific_producibility, " kWh/kWp"),
            'net_energy': format_range(net_energy, " kWh/m²"),
            'system_efficiency': format_range(system_efficiency, "%", digits=1),
            'losses_percentage': format_range(losses_percentage, "%", digits=1),
        }

    def get_subfields_annual_energy_production_table_data(self, ao1_subfields):
        """
        Genera i dati per la tabella dell'energia elettrica teoricamente ottenibile
        per ogni sottocampo.

        Returns:
            list: Lista di tuple (sottocampo, potenza_installata, energia_prodotta)
        """

        generator = self.data.get('generator', {})

        if not ao1_subfields or not generator:
            return []

        table_data = []
        total_power = 0.0
        total_energy = 0.0

        # Processa ogni sottocampo
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    # Ottieni il nome utente del sottocampo
                    user_subfield_name = subfield_data_gen.get('name', '')
                    display_name = f"{subfield_name} {user_subfield_name}" if user_subfield_name else subfield_name

                    # Ottieni la potenza installata per questo sottocampo
                    subfield_power = self.data['sizing'][field_name][subfield_name]['total_power']

                    # Ottieni l'energia prodotta annualmente dal sottocampo
                    subfield_data = ao1_subfields[subfield_name]
                    annual_energy_production = subfield_data.get('annual_energy_production', (0, ''))

                    # Se è una tupla (valore, unità), prendi il valore
                    if isinstance(annual_energy_production, (list, tuple)) and len(annual_energy_production) > 0:
                        energy_value = annual_energy_production[0]
                    else:
                        energy_value = annual_energy_production

                    # Formatta i valori
                    try:
                        energy_float = float(energy_value)
                        # Calcola l'energia proporzionalmente alla potenza del sottocampo
                        # Se l'energia è per kWp, moltiplica per la potenza del sottocampo
                        actual_energy = energy_float * subfield_power
                    except (ValueError, TypeError):
                        print(f"Errore nella conversione dell'energia per {subfield_name}: {energy_value}")
                        actual_energy = 0.0

                    table_data.append(
                        (display_name, subfield_power, actual_energy))
                    total_power += subfield_power
                    total_energy += actual_energy
        if table_data:
            table_data.append(("Totale", total_power, total_energy))

        return table_data

    def get_subfields_annual_net_energy_slogans(self, ao1_subfields):
        """
        Genera slogan per ogni sottocampo con la classificazione dell'energia netta annua.

        Returns:
            list: Lista di slogan per ogni sottocampo nel formato:
                  "Sottocampo A1 'Nome': un valore di X kWh/m²/anno rientra nella classe Y. Descrizione."
        """
        # Definisce le soglie e i commenti per la classificazione (da ao1/annualnetenergyclassification.py)
        thresholds = {
            "Molto bassa": (900, "L'area presenta una bassissima irradiazione, poco favorevole per impianti fotovoltaici."),
            "Bassa": (1100, "Irradianza risulta modesta e la conseguente resa energetica limitata; adatta solo per progetti locali e ben ottimizzati."),
            "Media": (1300, "Il sito di installazione presenta un contesto di condizioni energetiche moderate, la fattibilità economica può essere accettabile per progetti residenziali e commerciali."),
            "Alta": (1500, "Buona irradiazione, alta efficienza e resa economica interessante per gli impianti fotovoltaici anche di medie e grandi dimensioni."),
            "Molto Alta": (float('inf'), "Questo indica che la località ha un'ottima esposizione solare e condizioni favorevoli per la produzione di energia solare. Un impianto fotovoltaico in questa area sarebbe in grado di produrre una quantità significativa di energia elettrica, rendendo l'investimento molto conveniente.")
        }

        generator = self.data.get('generator', {})

        if not ao1_subfields or not generator:
            return []

        slogans = []

        # Processa ogni sottocampo
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    # Ottieni il nome utente del sottocampo
                    user_subfield_name = subfield_data_gen.get('name', '')

                    # Ottieni l'energia netta annua per questo sottocampo
                    subfield_data = ao1_subfields[subfield_name]
                    annual_net_energy = subfield_data.get('annual_net_energy', (0, ''))

                    # Estrai il valore numerico
                    if isinstance(annual_net_energy, (list, tuple)) and len(annual_net_energy) > 0:
                        energy_value = annual_net_energy[0]
                    else:
                        energy_value = annual_net_energy

                    try:
                        energy_float = float(energy_value)
                    except (ValueError, TypeError):
                        print(f"Errore nella conversione del valore per {subfield_name}: {energy_value}")
                        continue

                    # Classifica il valore
                    energy_class = None
                    energy_comment = ""

                    for threshold_label, (threshold_value, threshold_comment) in thresholds.items():
                        if energy_float < threshold_value:
                            energy_class = threshold_label
                            energy_comment = threshold_comment
                            break

                    # Genera lo slogan
                    if energy_class:
                        if user_subfield_name:
                            slogan = f'Sottocampo {subfield_name} "{user_subfield_name}": un valore di {energy_float:.2f} kWh/m²/anno rientra nella classe {energy_class}. {energy_comment}'
                        else:
                            slogan = f'Sottocampo {subfield_name}: un valore di {energy_float:.2f} kWh/m²/anno rientra nella classe {energy_class}. {energy_comment}'

                        slogans.append(slogan)
                    else:
                        print(
                            f"Impossibile classificare il valore per {subfield_name}: {energy_float}")

        return slogans

    def get_subfields_system_efficiency_slogans(self, ao1_subfields):
        """
        Genera slogan per ogni sottocampo con la classificazione dell'efficienza del sistema.

        Returns:
            list: Lista di slogan per ogni sottocampo nel formato:
                  "Efficienza percentuale del A1 Nome: X%. A1 Nome: Questi valori di efficienza percentuale rientrano nella classe Y. Descrizione."
        """
        # Definisce le soglie e i commenti per la classificazione (da ao1/systemefficiencyclassification.py)
        thresholds = {
            "Molto bassa": (65, "Generalmente gli impianti tipici di questa classe presentano una notevole "
                                "quantità di perdite. Questa bassa efficienza può essere dovuta a una serie di "
                                "problemi come un alto grado di ombreggiamento, un'inclinazione subottimale dei "
                                "pannelli, moduli fotovoltaici di qualità scadente, o inverter inefficaci. Anche "
                                "temperature elevate senza adeguata ventilazione possono ridurre sensibilmente le "
                                "prestazioni."),
            "Bassa": (70, "In questa fascia, l'efficienza è ancora inferiore rispetto alle medie del settore, "
                          "suggerendo un'installazione con condizioni non ottimali o componenti di media qualità."),
            "Media": (75, "Un impianto con efficienza media presenta una discreta capacità di conversione, con "
                          "perdite contenute grazie a un'installazione ragionevolmente ottimizzata e a componenti "
                          "standard. Le perdite, in questo caso, sono prevalentemente legate a fattori comuni, "
                          "come un certo grado di ombreggiamento o temperature elevate che impattano l'efficienza "
                          "dei moduli."),
            "Alta": (80, "Un'efficienza alta denota un sistema fotovoltaico ben progettato, con perdite ridotte al "
                         "minimo. Gli impianti in questa fascia generalmente sfruttano orientamento e inclinazione "
                         "ottimali, pannelli di alta qualità e inverter efficienti, oltre a una gestione delle "
                         "ombre ottimizzata e una buona ventilazione."),
            "Molto Alta": (float('inf'), "Questa classe rappresenta l'eccellenza nell'efficienza di conversione "
                                         "fotovoltaica, con perdite minime. Gli impianti in questa categoria "
                                         "sfruttano i migliori materiali e tecnologie, con un'installazione "
                                         "perfettamente ottimizzata per irraggiamento e inclinazione, un "
                                         "eccellente sistema di gestione dell'ombreggiamento e soluzioni per "
                                         "ridurre le perdite termiche e di conversione al minimo.")
        }

        generator = self.data.get('generator', {})

        if not ao1_subfields or not generator:
            return []

        slogans = []

        # Processa ogni sottocampo
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    # Ottieni il nome utente del sottocampo
                    user_subfield_name = subfield_data_gen.get('name', '')

                    # Ottieni l'efficienza del sistema per questo sottocampo
                    subfield_data = ao1_subfields[subfield_name]
                    system_efficiency = subfield_data.get(
                        'system_efficiency', (0, ''))

                    # Estrai il valore numerico
                    if isinstance(system_efficiency, (list, tuple)) and len(system_efficiency) > 0:
                        efficiency_value = system_efficiency[0]
                    else:
                        efficiency_value = system_efficiency

                    try:
                        efficiency_float = float(efficiency_value)
                    except (ValueError, TypeError):
                        print(
                            f"Errore nella conversione del valore per {subfield_name}: {efficiency_value}")
                        continue

                    # Classifica il valore
                    efficiency_class = None
                    efficiency_comment = ""

                    for threshold_label, (threshold_value, threshold_comment) in thresholds.items():
                        if efficiency_float < threshold_value:
                            efficiency_class = threshold_label
                            efficiency_comment = threshold_comment
                            break

                    # Genera lo slogan nel formato richiesto
                    if efficiency_class:
                        if user_subfield_name:
                            # Prima parte: "Efficienza percentuale del A1 Nome: X%."
                            first_part = f"Efficienza percentuale del {subfield_name} {user_subfield_name}: {efficiency_float:.2f}%."
                            # Seconda parte: "A1 Nome: Questi valori di efficienza percentuale rientrano nella classe Y. Descrizione."
                            second_part = f"{subfield_name} {user_subfield_name}: Questi valori di efficienza percentuale rientrano nella classe {efficiency_class}. {efficiency_comment}"
                        else:
                            # Prima parte: "Efficienza percentuale del A1: X%."
                            first_part = f"Efficienza percentuale del {subfield_name}: {efficiency_float:.2f}%."
                            # Seconda parte: "A1: Questi valori di efficienza percentuale rientrano nella classe Y. Descrizione."
                            second_part = f"{subfield_name}: Questi valori di efficienza percentuale rientrano nella classe {efficiency_class}. {efficiency_comment}"

                        # Combina le due parti
                        slogan = f"{first_part}\n{second_part}"
                        slogans.append(slogan)
                    else:
                        print(
                            f"Impossibile classificare il valore per {subfield_name}: {efficiency_float}")

        return slogans

    def get_subfields_emission_reduction_table_data(self, ao1_subfields):
        """
        Calcola i valori di riduzione delle emissioni (TEP e CO2) per ogni sottocampo.

        Returns:
            tuple: (table_data, totals) dove:
                - table_data: Lista di tuple (sottocampo, tep_value, co2_value)
                - totals: Tuple (total_tep, total_co2)
        """
        # Costanti per i calcoli (da ao1/data/parameter_values.py)
        SYSTEM_LIFETIME = 20.0  # anni
        CTEP = 11630.0  # kWh/TEP
        EFCO2 = 0.23  # kg CO2/kWh
        EFCH4 = 0.015  # kg CH4/kWh
        EFN2O = 0.0002  # kg N2O/kWh
        CH4_CO2 = 28.0  # fattore conversione CH4 -> CO2
        N2O_CO2 = 273.0  # fattore conversione N2O -> CO2

        generator = self.data.get('generator', {})

        if not ao1_subfields or not generator:
            return [], (0, 0)

        # Usa i dati della tabella dell'energia elettrica per ottenere i valori di produzione
        energy_production_table_data = self.get_subfields_annual_energy_production_table_data(
            ao1_subfields)

        table_data = []
        total_tep = 0.0
        total_co2 = 0.0

        # Processa ogni sottocampo
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    user_subfield_name = subfield_data_gen.get('name', '')

                    # Nome del sottocampo
                    display_name = f"{subfield_name} {user_subfield_name}" if user_subfield_name else subfield_name

                    # Trova l'energia elettrica prodotta annualmente da questo sottocampo
                    annual_energy_production = 0.0
                    for table_row in energy_production_table_data:
                        if len(table_row) >= 3 and subfield_name in table_row[0]:
                            # Terza colonna: energia [kWh/anno]
                            annual_energy_production = float(table_row[2])
                            break

                    if annual_energy_production > 0:
                        # Calcolo TEP (Tonnellate Equivalenti di Petrolio)
                        # TEP = (energia_annua * anni_vita) / fattore_conversione
                        tep_reduction = (
                            annual_energy_production * SYSTEM_LIFETIME) / CTEP

                        # Calcolo riduzione CO2 (seguendo la logica di GreenHouseGasesReduction)
                        # 1. Calcolo emissioni evitate annue per gas
                        co2_reduction_annual = annual_energy_production * EFCO2
                        ch4_reduction_annual = annual_energy_production * EFCH4
                        n2o_reduction_annual = annual_energy_production * EFN2O

                        # 2. Conversione CH4 e N2O in CO2 equivalente
                        ch4_co2_eq_reduction_annual = ch4_reduction_annual * CH4_CO2
                        n2o_co2_eq_reduction_annual = n2o_reduction_annual * N2O_CO2

                        # 3. Totale GHG evitati annui
                        ghg_co2_eq_reduction_annual = co2_reduction_annual + \
                            ch4_co2_eq_reduction_annual + n2o_co2_eq_reduction_annual

                        # 4. Calcolo GHG totale in 20 anni e conversione in tonnellate
                        ghg_co2_eq_reduction_total = ghg_co2_eq_reduction_annual * SYSTEM_LIFETIME
                        co2_reduction_tons = ghg_co2_eq_reduction_total / 1000.0  # da kg a tonnellate

                        # Aggiungi ai totali
                        total_tep += tep_reduction
                        total_co2 += co2_reduction_tons

                        # Aggiungi alla tabella
                        table_data.append(
                            (display_name, tep_reduction, co2_reduction_tons))
        # Aggiungi la riga totale se ci sono dati
        if table_data:
            table_data.append(("Totale", total_tep, total_co2))

        return table_data, (total_tep, total_co2)

    def get_subfields_annual_loss_percentage_classifications(self, ao1_subfields):
        """
        Genera le classificazioni delle perdite totali per ogni sottocampo.

        Returns:
            list: Lista di tuple (sottocampo, valore_perdita, classe, commento)
        """
        # Definisce le soglie e i commenti per la classificazione (da ao1/annuallosspercentageclassification.py)
        thresholds = {
            "Molto bassa": (10, "In questo caso le perdite di sistema molto basse rappresentano una condizione "
                            "ideale e sono indice di un impianto altamente ottimizzato."),
            "Bassa": (15, "Le perdite di sistema in questa classe sono lievemente superiori rispetto alla classe "
                      "-Molto Bassa-, ma sono comunque indicative di un impianto ben progettato composto da "
                      "attrezzature di qualità."),
            "Media": (20, "Una classe di perdite medie indica che l'impianto è soggetto a inefficienze moderate "
                      "che, sebbene non compromettano gravemente le performance complessive, segnalano possibili "
                      "margini di miglioramento."),
            "Alta": (25, "Questa classe indica perdite di sistema rilevanti che compromettono significativamente "
                     "le prestazioni dell'impianto fotovoltaico."),
            "Molto Alta": (float('inf'), "Le perdite molto alte indicano una situazione critica in cui l'impianto "
                           "ha prestazioni gravemente compromesse. In questa classe, oltre il 25% dell'energia "
                           "teorica viene dispersa o non convertita sufficientemente.")
        }

        generator = self.data.get('generator', {})

        if not ao1_subfields or not generator:
            return []

        classifications = []

        # Processa ogni sottocampo
        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data_gen in field_data.items():  # "A1", "A2", "B1", "B2"
                if subfield_name in ao1_subfields:
                    # Ottieni il nome utente del sottocampo
                    user_subfield_name = subfield_data_gen.get('name', '')

                    # Ottieni la percentuale di perdite annuali per questo sottocampo
                    subfield_data = ao1_subfields[subfield_name]
                    annual_loss_percentage = subfield_data.get(
                        'annual_loss_percentage', (0, ''))

                    # Estrai il valore numerico
                    if isinstance(annual_loss_percentage, (list, tuple)) and len(annual_loss_percentage) > 0:
                        loss_value = annual_loss_percentage[0]
                    else:
                        loss_value = annual_loss_percentage

                    try:
                        loss_float = float(loss_value)
                    except (ValueError, TypeError):
                        print(
                            f"Errore nella conversione del valore per {subfield_name}: {loss_value}")
                        continue

                    # Classifica il valore
                    loss_class = None
                    loss_comment = ""

                    for threshold_label, (threshold_value, threshold_comment) in thresholds.items():
                        if loss_float < threshold_value:
                            loss_class = threshold_label
                            loss_comment = threshold_comment
                            break

                    # Aggiungi alla lista delle classificazioni
                    if loss_class:
                        display_name = f"{subfield_name} {user_subfield_name}" if user_subfield_name else subfield_name
                        classifications.append(
                            (display_name, loss_float, loss_class, loss_comment))
                    else:
                        print(
                            f"Impossibile classificare il valore per {subfield_name}: {loss_float}")

        return classifications

    def process_pipelines(self):
        """Lancia le pipelines di ao1 (sole10349, losses, energy) per ogni sottocampo."""

        # Controlli di sicurezza per le chiavi richieste
        try:
            latitude = self.data['latitude_float']
            longitude = self.data['longitude_float']
            albedo = self.data['albedo_float']
            shading_horizon = float(self.data['shading_horizon'])
        except KeyError as e:
            print(f"Errore: chiave mancante nel dizionario data: {e}")
            return {}
        except (ValueError, TypeError) as e:
            print(f"Errore nella conversione dei valori: {e}")
            return {}

        # Ottieni i sottocampi dal generator
        generator = self.data.get('generator', {})

        # Processa ogni sottocampo
        output = {}
        all_subfields_data = {}
        if not self.data['sizing']:
            return {}

        for field_name, field_data in generator.items():  # "A", "B"
            for subfield_name, subfield_data in field_data.items():  # "A1", "A2", "B1", "B2"
                # Estrai i parametri specifici del sottocampo
                tilt = float(subfield_data.get('inclination', 30.0))
                azimuth = float(subfield_data.get('azimuth', 0.0))
                shading_obstacles = float(subfield_data.get('shading_obstacles', 0.0))
                # Prendere la potenza installata nel sottocampo dal dimensionamento
                subfield_peak_power = self.data['sizing'][field_name][subfield_name].get('total_power')
                user_input = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'tilt': tilt,
                    'azimuth': azimuth,
                    'albedo': albedo,
                    'shading_obstacle': shading_obstacles,
                    'shading_horizon': shading_horizon,
                    "nominal_peak_power": subfield_peak_power
                }

                db = DataBank(user_input)
                ao1_subfield = self.run_pipelines(db)

                if ao1_subfield:
                    # Calcola i valori massimi per i grafici
                    data_1 = ao1_subfield.get('monthly_net_energy', {})
                    data_2 = ao1_subfield.get('monthly_energy_yield', {})
                    data_3 = ao1_subfield.get('monthly_plane_of_array_irradiance', {})

                    monthly_net_energy_chart_max = self.get_max_for_chart(data_1)
                    monthly_energy_yield_chart_max = self.get_max_for_chart(data_2)
                    monthly_plane_of_array_irradiance_chart_max = self.get_max_for_chart(data_3)

                    ao1_subfield["monthly_net_energy_chart_max"] = monthly_net_energy_chart_max
                    ao1_subfield["monthly_energy_yield_chart_max"] = monthly_energy_yield_chart_max
                    ao1_subfield["monthly_plane_of_array_irradiance_chart_max"] = monthly_plane_of_array_irradiance_chart_max

                    # Salva i risultati per questo sottocampo
                    all_subfields_data[subfield_name] = ao1_subfield
                else:
                    print(f"  Errore nel calcolo per {subfield_name}")

        # Salva tutti i risultati dei sottocampi

        if all_subfields_data:
            output['ao1'] = {"ao1_subfields": all_subfields_data}

            # Opzionalmente, calcola anche un risultato aggregato
            # Per ora, usa il primo sottocampo come risultato principale per compatibilità
            first_subfield = list(all_subfields_data.values())[0]
            output["ao1"]['first_subfield'] = first_subfield

            # Calcola ????
            total_annual_irradiance = self.get_max_irradiancy_energy(all_subfields_data)

            # Calcola la total_net_energy sommando tutti i sottocampi
            total_net_energy_data = self.get_total_net_energy(all_subfields_data)

            # Calcola la total_energy_production sommando tutti i sottocampi
            total_energy_production = self.get_total_energy_production(all_subfields_data)

            # Calcola una serie di range min-max per valori solari dei sottocampi
            range_solar_data = self.str_range_subfield_solar_data(all_subfields_data)

            # Calcola i valori totali di riduzione delle emissioni
            ghg_reduction, tep_reduction = self.get_total_emission_reduction(all_subfields_data)

            # Genera gli slogan per ogni sottocampo
            subfields_slogans = self.get_subfields_annual_net_energy_slogans(all_subfields_data)

            # Genera i dati della tabella dell'energia elettrica teoricamente ottenibile
            energy_production_table_data = self.get_subfields_annual_energy_production_table_data(all_subfields_data)

            # Genera gli slogan per l'efficienza del sistema
            system_efficiency_slogans = self.get_subfields_system_efficiency_slogans(all_subfields_data)

            # Genera i dati della riduzione delle emissioni
            emission_reduction_table_data, emission_reduction_totals = self.get_subfields_emission_reduction_table_data(
                all_subfields_data)

            # Genera le classificazioni delle perdite totali per ogni sottocampo
            annual_loss_percentage_classifications = self.get_subfields_annual_loss_percentage_classifications(
                all_subfields_data)

            # Salva i risultati nel primo sottocampo per compatibilità
            output['ao1']["total_annual_irradiance"] = total_annual_irradiance
            output['ao1']["total_energy_production"] = total_energy_production

            output['ao1']['range_module_solar_radiation'] = range_solar_data['module_solar_radiation']
            output['ao1']['range_specific_producibility'] = range_solar_data['specific_producibility']
            output['ao1']['range_net_energy'] = range_solar_data['net_energy']
            output['ao1']['range_system_efficiency'] = range_solar_data['system_efficiency']
            output['ao1']['range_losses_percentage'] = range_solar_data['losses_percentage']
            output['ao1']['ghg_co2_reduction'] = ghg_reduction
            output['ao1']['tep_reduction'] = tep_reduction

            output['ao1']["total_annual_net_energy"] = total_net_energy_data['total_annual_net_energy']
            output['ao1']["total_monthly_net_energy"] = total_net_energy_data['total_monthly_net_energy']
            output['ao1']["subfields_annual_net_energy_slogans"] = subfields_slogans
            output['ao1']["subfields_annual_energy_production_table_data"] = energy_production_table_data
            output['ao1']["subfields_system_efficiency_slogans"] = system_efficiency_slogans
            output['ao1']["emission_reduction_table_data"] = emission_reduction_table_data
            output['ao1']["emission_reduction_totals"] = emission_reduction_totals
            output['ao1']["subfields_annual_loss_percentage_classifications"] = annual_loss_percentage_classifications
        return output
