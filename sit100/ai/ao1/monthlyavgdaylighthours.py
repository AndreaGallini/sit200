# Arancione SOLE 10 ore di sole giorno, media mensile

from .concept import Measure, MeasureDerivation, months
import math
from datetime import datetime


class MonthlyAvgDaylightHours(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'latitude': the_input_data['latitude']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'monthly_avg_daylight_hours': {}
        }

    def validate(self):
        if self.input['latitude'] is None:
            return False
        if not isinstance(self.input['latitude'], Measure):
            return False
        return True

    def compute(self):
        def ore_luce_per_mese(latitudine):
            """
            Calcola il fotoperiodo: numero medio di ore di luce al giorno per ogni mese in base alla latitudine.

            :param latitudine: latitudine in gradi (positiva per il nord, negativa per il sud).
            :return: dizionario con il numero medio di ore di luce al giorno per ciascun mese.
            """

            # Lista di giorni medi del mese (intorno al 15 di ogni mese) (da norma UNI10349)
            # giorni_medi_mese = [17, 16, 16, 15, 15, 11, 17, 16, 15, 15, 14, 10]

            # Lista valori del giorno dell’anno considerato (n) - Giorno dell’anno n (da norma UNI10349)
            giorno_anno = [17, 47, 75, 105, 135, 162, 198, 228, 258, 288, 318, 344]

            ore_luce_mensili = {}

            for mese in range(1, 13):

                # Calcola il giorno dell'anno (da 1 a 365)
                giorno_annuale = giorno_anno[mese - 1]

                # Calcola la declinazione solare per il giorno dell'anno (23.45 da norma UNI10349)
                declinazione_solare = 23.45 * math.sin(math.radians((360 / 365) * (giorno_annuale - 81)))

                # Calcola l'angolo orario del tramonto
                latitudine_rad = math.radians(latitudine)
                declinazione_rad = math.radians(declinazione_solare)
                cos_omega = -math.tan(latitudine_rad) * math.tan(declinazione_rad)

                if cos_omega >= 1:
                    # Notte polare (nessun giorno)
                    ore_luce = 0.0
                elif cos_omega <= -1:
                    # Giorno polare (24 ore di luce)
                    ore_luce = 24.0
                else:
                    # Calcolo delle ore di luce
                    omega = math.acos(cos_omega)  # angolo orario in radianti
                    ore_luce = (2 * omega / math.pi) * 12  # conversione in ore

                # Salva il risultato nel dizionario
                month_name_list = list(months.keys())
                ore_luce_mensili[month_name_list[mese-1]] = Measure("h", round(ore_luce, 2))

            return ore_luce_mensili

        latitudine = self.input['latitude'].value
        monthly_avg_daylight_hours = ore_luce_per_mese(latitudine)
        self.output['monthly_avg_daylight_hours'] = monthly_avg_daylight_hours


if __name__ == '__main__':
    the_target = MonthlyAvgDaylightHours({
        "latitude": Measure("°", 41.9028),
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
