"""DataBankKeope: classe che si occupa dello stoccaggio dei dati dell'intera pipeline.
Responsabilità: si occupa solo della memorizzazione."""


class KeopeBank:
    def __init__(self):
        """Dizionari per memorizzare i vari tipi di dati."""
        self._data = {}
        self._string_placeholders = {}
        self._xml_placeholders = {}
        self._xml_data = {}

    def set_data(self, key, value):
        """Imposta un placeholder nel _data."""
        self._data[key] = value

    def add_data(self, data):
        """ Unisce un dizionario a quello esistente."""
        self._data.update(data)  # Fonde il dizionario nel campo _data

    def get_data(self, key):
        """Recupera un dato da _data."""
        return self._data.get(key, None)

    def get_all_data(self):
        return self._data

    def set_string_placeholder(self, key, value):
        """Imposta un placeholder nel _string_placeholders."""
        self._string_placeholders[key] = value

    def add_string_placeholders(self, data):
        """Aggiunge un dizionario di placeholder all'esistente _string_placeholders."""
        self._string_placeholders.update(data)

    def get_string_placeholder(self, key):
        """Recupera un placeholder da _string_placeholders."""
        return self._string_placeholders.get(key, None)

    def get_string_placeholders(self):
        """Recupera tutti i _string_placeholders."""
        return self._string_placeholders

    def set_xml_placeholder(self, key, value):
        """Imposta un placeholder nel _xml_placeholders."""
        self._xml_placeholders[key] = value

    def add_xml_placeholders(self, data):
        """Aggiunge un dizionario di placeholder all'esistente _xml_placeholders."""
        self._xml_placeholders.update(data)

    def get_xml_placeholder(self, key):
        """Recupera un placeholder da _xml_placeholders."""
        return self._xml_placeholders.get(key, None)

    def get_xml_placeholders(self):
        """Recupera tutti i _xml_placeholders."""
        return self._xml_placeholders

    def set_xml_data(self, key, xml_value):
        """Imposta un dato formattato come XML in xml_data."""
        self._xml_data[key] = xml_value

    def add_xml_data(self, data):
        """Aggiungi dati XML a xml_data."""
        self._xml_data.update(data)

    def get_xml_data(self, key):
        """Recupera un dato formattato come XML dal xml_data."""
        return self._xml_data.get(key, None)

    def get_all_xml(self):
        return self._xml_data

    def get_all_keopebank(self):
        return {
            "data": self._data,
            "string_placeholders": self._string_placeholders,
            "xml_placeholders": self._xml_placeholders,
            "xml_data": self._xml_data
        }

    def to_dict(self):
        """Converte il databank in un dizionario."""
        return {
            "data": self._data,
            "string_placeholders": self._string_placeholders,
            "xml_placeholders": self._xml_placeholders,
            "xml_data": self._xml_data,
        }

    @classmethod
    def from_dict(cls, data_dict):
        """Crea una KeopeBank da un dizionario."""
        keopebank = cls()
        keopebank._data = data_dict.get("data", {})
        keopebank._string_placeholders = data_dict.get("string_placeholders", {})
        keopebank._xml_placeholders = data_dict.get("xml_placeholders", {})
        keopebank._xml_data = data_dict.get("xml_data", {})

        return keopebank
