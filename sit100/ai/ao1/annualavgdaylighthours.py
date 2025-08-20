# Arancione SOLE 11 ore di sole giorno, media annuale (ponderazione medie annuali)

from .concept import Measure, MeasureDerivation, ClimatePosition, months
from .utils import log
import math
from datetime import datetime


class AnnualAvgDaylightHours(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_avg_daylight_hours': the_input_data['monthly_avg_daylight_hours']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'annual_avg_daylight_hours': Measure("h", 0.0)
        }

    def validate(self):
        if self.input['monthly_avg_daylight_hours'] is None:
            log("ERROR", "missing input value monthly_avg_daylight_hours")
            return False
        if len(self.input['monthly_avg_daylight_hours']) != 12:
            log("ERROR", "missing some monthly input values in monthly_avg_daylight_hours")
            return False
        for month in months:
            if month not in self.input['monthly_avg_daylight_hours']:
                log("ERROR", f"missing {month} input values in monthly_avg_daylight_hours")
                return False
            if not isinstance(self.input['monthly_avg_daylight_hours'][month], Measure):
                log("ERROR", f"{month} input values in monthly_avg_daylight_hours is not a Measure")
                return False
        return True

    def compute(self):
        def fotoperiodo_medio_annuale(ore_luce_mensili):
            """
            Calcola il fotoperiodo medio annuale (ore di luce medie giornaliere su base annuale)
            utilizzando le ore di luce medie giornaliere per ciascun mese e ponderando per il numero di giorni del mese.

            :param ore_luce_mensili: Dizionario con le ore di luce medie giornaliere per ciascun mese (es. {1: ore_gennaio, ...}).
            :return: Fotoperiodo medio annuale in ore.
            """

            # Numero di giorni per ciascun mese (considerando un anno non bisestile)
            giorni_per_mese = {1: 31, 2: 28.25, 3: 31, 4: 30, 5: 31, 6: 30,
                               7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

            # Calcola la somma ponderata delle ore di luce
            somma_ponderata = sum(ore_luce_mensili[mese] * giorni_per_mese[mese] for mese in range(1, 13))

            # Divide per 365 per ottenere la media annuale giornaliera
            il_fotoperiodo_medio_annuale = somma_ponderata / 365

            return round(il_fotoperiodo_medio_annuale, 2)
        monthly_avg_daylight_hours = {i: value.value for i, value in enumerate(self.input['monthly_avg_daylight_hours'].values(), 1)}
        annual_avg_daylight_hours = fotoperiodo_medio_annuale(monthly_avg_daylight_hours)
        self.output['annual_avg_daylight_hours'] = Measure("h", annual_avg_daylight_hours)


if __name__ == '__main__':
    the_target = AnnualAvgDaylightHours({
        "monthly_avg_daylight_hours": {
            'GEN': Measure("h", 9.33),
            'FEB': Measure("h", 10.41),
            'MAR': Measure("h", 11.71),
            'APR': Measure("h", 13.14),
            'MAG': Measure("h", 14.37),
            'GIU': Measure("h", 15.00),
            'LUG': Measure("h", 14.71),
            'AGO': Measure("h", 13.65),
            'SET': Measure("h", 12.27),
            'OTT': Measure("h", 10.84),
            'NOV': Measure("h", 9.61),
            'DIC': Measure("h", 9.01)
        },
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
