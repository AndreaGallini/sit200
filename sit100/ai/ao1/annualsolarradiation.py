# arancione SOLE 8 radiazione solare annua sul piano dei moduli
from .concept import Measure, MeasureDerivation


class AnnualSolarRadiation(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                'monthly_plane_of_array_irradiance': the_input_data['monthly_plane_of_array_irradiance']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'annual_solar_radiation': Measure("kWh/m2/anno", 41.96)
        }

    def validate(self):
        # 12 misure con unità corretta
        return True

    def compute(self):
        monthly_plane_of_array_irradiance = self.input['monthly_plane_of_array_irradiance']
        annual_solar_radiation = sum([mai.value for mai in monthly_plane_of_array_irradiance.values()])
        annual_solar_radiation = round(annual_solar_radiation, 2)
        self.output['annual_solar_radiation'] = Measure("kWh/m2/anno", annual_solar_radiation)


if __name__ == '__main__':
    the_target = AnnualSolarRadiation({
                'monthly_plane_of_array_irradiance': {
                    'GEN': Measure("kWh/m2/mese", 3.08),
                    'FEB': Measure("kWh/m2/mese", 3.18),
                    'MAR': Measure("kWh/m2/mese", 3.28),
                    'APR': Measure("kWh/m2/mese", 3.38),
                    'MAG': Measure("kWh/m2/mese", 3.48),
                    'GIU': Measure("kWh/m2/mese", 3.68),
                    'LUG': Measure("kWh/m2/mese", 4.08),
                    'AGO': Measure("kWh/m2/mese", 3.98),
                    'SET': Measure("kWh/m2/mese", 3.78),
                    'OTT': Measure("kWh/m2/mese", 3.58),
                    'NOV': Measure("kWh/m2/mese", 3.38),
                    'DIC': Measure("kWh/m2/mese", 3.08)
                }
            })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
