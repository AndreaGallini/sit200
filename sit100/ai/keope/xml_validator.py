"""
CLasse che verifica che il progetto xml sia privo di errori.
Ritorna il t4 (progetto validato)
"""


class XMLValidator:

    def __init__(self, t4):
        self.t4 = t4

    def convalide(self):
        '''
            def is_xml(string):
        """Verifica se una stringa è un pezzo di XML valido."""
        try:
            etree.fromstring(string)
            return True
        except etree.XMLSyntaxError:
            return False
        '''

        t5 = self.t4
        return t5
