# arancione EE 6 efficienza di sistema
from .concept import Measure, MeasureDerivation


class SystemEfficiency(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_energy_yield': the_input_data['annual_energy_yield'],
                'annual_net_energy': the_input_data['annual_net_energy']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "system_efficiency": Measure("%", 0.0)
        }

    def validate(self):
        # controllare unità di misura
        return True

    def compute(self):
        annual_energy_yield = self.input['annual_energy_yield'].value
        annual_net_energy = self.input['annual_net_energy'].value
        system_efficiency = round(annual_energy_yield / annual_net_energy * 100, 2)
        self.output["system_efficiency"] = Measure("%", system_efficiency)


if __name__ == '__main__':
    the_target = SystemEfficiency({
        'annual_energy_yield': Measure("kWh/kWp", 9000.0),
        'annual_net_energy': Measure("kWh/kWp", 10000.0)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
