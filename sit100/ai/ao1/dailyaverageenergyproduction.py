# verde Q2 produzione giornaliera dell'impianto FV
from concept import Measure, MeasureDerivation
import utils


class DailyAverageEnergyProduction(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_energy_production': the_input_data['annual_energy_production'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "daily_average_energy_production": Measure("kWh", 0.0)
        }

    def validate(self):
        key = 'annual_energy_production'
        value = self.input[key]
        if not isinstance(value, Measure):
            return f"Errore: '{key}' non è una misura."
        if not value.unit == 'kWh':
            return f"Errore: L'unità di misura per '{key}' deve essere kWh."
        if not isinstance(value.value, float):
            return f"Errore: Il valore per '{key}' deve essere un float."
        return True

    def compute(self):
        annual_energy_production = self.input['annual_energy_production'].value
        daily_average_energy_production = utils.proper_round(annual_energy_production / 3655)
        self.output['daily_average_energy_production'] = Measure("kWh", daily_average_energy_production)


if __name__ == '__main__':
    the_target = DailyAverageEnergyProduction({
        'annual_energy_production': Measure("kWh", 365000.0),
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
