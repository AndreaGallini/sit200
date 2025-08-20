# arancione EE 1 Energia utile mensile
from .concept import Measure, MeasureDerivation, months


class MonthlyNetEnergy(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_plane_of_array_irradiance': the_input_data['monthly_plane_of_array_irradiance'],
                'fixed_sys_monthly_shading_loss': the_input_data['fixed_sys_monthly_shading_loss']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "monthly_net_energy": {month: Measure("kWg/m2/mese", 0.0) for month in months}
        }

    def validate(self):
        # 12 misure di energia utile con unità corretta, lo stesso per la perdita da ombreggiamento
        return True

    def compute(self):
        monthly_plane_of_array_irradiance = self.input['monthly_plane_of_array_irradiance']
        fixed_sys_monthly_shading_loss = self.input['fixed_sys_monthly_shading_loss']
        monthly_net_energy = {}
        for mese in months:
            irradiance = monthly_plane_of_array_irradiance[mese].value
            shading_loss = fixed_sys_monthly_shading_loss[mese].value
            monthly_net_energy[mese] = (
                Measure("kWh/m2/mese", round(irradiance - shading_loss, 2))
            )
        self.output['monthly_net_energy'] = monthly_net_energy


if __name__ == '__main__':
    the_target = MonthlyNetEnergy({
        'monthly_plane_of_array_irradiance': {
            "GEN": Measure("kWh/m2/mese", 150.0),
            "FEB": Measure("kWh/m2/mese", 140.0),
            "MAR": Measure("kWh/m2/mese", 145.0),
            "APR": Measure("kWh/m2/mese", 140.0),
            "MAG": Measure("kWh/m2/mese", 140.0),
            "GIU": Measure("kWh/m2/mese", 125.0),
            "LUG": Measure("kWh/m2/mese", 120.0),
            "AGO": Measure("kWh/m2/mese", 110.0),
            "SET": Measure("kWh/m2/mese", 115.0),
            "OTT": Measure("kWh/m2/mese", 120.0),
            "NOV": Measure("kWh/m2/mese", 130.0),
            "DIC": Measure("kWh/m2/mese", 145.0),
        },
        'fixed_sys_monthly_shading_loss': {
            "GEN": Measure("kWh/m2/mese", 30.0),
            "FEB": Measure("kWh/m2/mese", 30.0),
            "MAR": Measure("kWh/m2/mese", 30.0),
            "APR": Measure("kWh/m2/mese", 30.0),
            "MAG": Measure("kWh/m2/mese", 30.0),
            "GIU": Measure("kWh/m2/mese", 30.0),
            "LUG": Measure("kWh/m2/mese", 30.0),
            "AGO": Measure("kWh/m2/mese", 30.0),
            "SET": Measure("kWh/m2/mese", 30.0),
            "OTT": Measure("kWh/m2/mese", 30.0),
            "NOV": Measure("kWh/m2/mese", 30.0),
            "DIC": Measure("kWh/m2/mese", 30.0),
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
