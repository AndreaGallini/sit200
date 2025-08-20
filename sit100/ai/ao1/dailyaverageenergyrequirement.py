# verde Q1 fabbisogno medio giornaliero
from concept import Measure, MeasureDerivation


class DailyAverageEnergyRequirement(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'daytime_average_energy_consumption': the_input_data['daytime_average_energy_consumption'],
                'nighttime_average_energy_consumption': the_input_data['nighttime_average_energy_consumption']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "daily_average_energy_requirement": Measure("kWh", 0.0)
        }

    def validate(self):
        for key in ['daytime_average_energy_consumption', 'nighttime_average_energy_consumption']:
            value = self.input[key]
            if not isinstance(value, Measure):
                return f"Errore: '{key}' non è una misura."
            if not value.unit == 'kWh':
                return f"Errore: L'unità di misura per '{key}' deve essere kWh."
            if not isinstance(value.value, float):
                return f"Errore: Il valore per '{key}' deve essere un float."
        return True

    def compute(self):
        daytime_average_energy_consumption = self.input['daytime_average_energy_consumption'].value
        nighttime_average_energy_consumption = self.input['nighttime_average_energy_consumption'].value
        daily_average_energy_requirement = daytime_average_energy_consumption + nighttime_average_energy_consumption
        self.output['daily_average_energy_requirement'] = Measure("kWh", daily_average_energy_requirement)


if __name__ == '__main__':
    the_target = DailyAverageEnergyRequirement({
        'daytime_average_energy_consumption': Measure("kWh/kWp", 3000.0),
        'nighttime_average_energy_consumption': Measure("kWh/kWp", 2000.0)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
