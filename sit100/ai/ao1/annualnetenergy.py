# arancione EE 2 energia utile annua
from .concept import Measure, MeasureDerivation


class AnnualNetEnergy(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_solar_radiation': the_input_data['annual_solar_radiation'],
                'fixed_sys_annual_shading_loss': the_input_data['fixed_sys_annual_shading_loss']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "annual_net_energy": Measure("kWh/m2/anno", 1250.0)
        }

    def validate(self):
        # verificare unità di misura
        return True

    def compute(self):
        annual_solar_radiation = self.input['annual_solar_radiation'].value
        fixed_sys_annual_shading_loss = self.input['fixed_sys_annual_shading_loss'].value
        annual_net_energy = round(annual_solar_radiation - fixed_sys_annual_shading_loss, 2)
        self.output['annual_net_energy'] = Measure("kWh/m2/anno", annual_net_energy)


if __name__ == '__main__':
    the_target = AnnualNetEnergy({
        'annual_solar_radiation': Measure("kWh/m2/anno", 1500.0),
        'fixed_sys_annual_shading_loss': Measure("kWh/m2/anno", 250.0)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
