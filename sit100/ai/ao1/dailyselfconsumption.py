# verde Q3 autoconsumo
from concept import Measure, MeasureDerivation
import utils


class DailySelfConsumption(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'daily_average_energy_production': the_input_data['daily_average_energy_production'],
                'daytime_self_consumption': the_input_data['daytime_self_consumption'],
                'ideal_average_daily_self_consumption': the_input_data['ideal_average_daily_self_consumption']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "daily_self_consumption_percentage": Measure("%", 0.0),
            "daily_self_consumption": Measure("kWh", 0.0),
        }

    def validate(self):
        for key in ['daily_average_energy_production', 'daytime_self_consumption']:
            value = self.input[key]
            if not isinstance(value, Measure):
                return f"Errore: '{key}' non è una misura."
            if not value.unit == 'kWh':
                return f"Errore: L'unità di misura per '{key}' deve essere kWh."
            if not isinstance(value.value, float):
                return f"Errore: Il valore per '{key}' deve essere un float."
        return True

    def compute(self):
        daily_average_energy_production = self.input['daily_average_energy_production'].value
        daytime_self_consumption = self.input['daytime_self_consumption'].value
        daily_self_consumption = utils.proper_round(
            daytime_self_consumption / daily_average_energy_production
            * 100)
        self.output['daily_self_consumption'] = Measure("%", daily_self_consumption)


if __name__ == '__main__':
    the_target = DailySelfConsumption({
        'daily_average_energy_production': Measure("kWh", 1000.0),
        'daytime_self_consumption': Measure("kWh", 800.0),
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
