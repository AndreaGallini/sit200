# arancione EE 8 producibilità giornaliera media annua
from .concept import Measure, MeasureDerivation


class DailyEnergyYield(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_energy_yield': the_input_data['annual_energy_yield']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "daily_energy_yield": Measure("kWh/kWp", 0.2)
        }

    def validate(self):
        # controllare unità di misura
        return True

    def compute(self):
        annual_energy_yield = self.input['annual_energy_yield'].value
        daily_energy_yield = round(annual_energy_yield / 365.25, 2)
        self.output["daily_energy_yield"] = Measure("kWh/giorno", daily_energy_yield)


if __name__ == '__main__':
    the_target = DailyEnergyYield({
        'annual_energy_yield': Measure("kWh/kWp", 120)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
