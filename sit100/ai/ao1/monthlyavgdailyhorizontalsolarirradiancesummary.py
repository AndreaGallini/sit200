# arancione SOLE 12 sommario irradiazione solare, anche riflessa, giornaliera media mensile
from .concept import Measure, MeasureDerivation, months, dict2text


class MonthlyAvgDailyHorizontalSolarIrradianceSummary(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.input = the_input_data
        """try:
            self.input = {
                'albedo': the_input_data['albedo'],
                'monthly_avg_daily_horizontal_irradiance': the_input_data['monthly_avg_daily_horizontal_irradiance'],
                'monthly_avg_daily_diffuse_horizontal_irradiance': the_input_data['monthly_avg_daily_diffuse_horizontal_irradiance'],
                'monthly_avg_daily_beam_horizontal_irradiance': the_input_data['monthly_avg_daily_beam_horizontal_irradiance']
            }
        except KeyError:
            print("missing input value")
            quit()"""
        self.output = {}

    def validate(self):
        return True
        for the_key, the_type in {
            'albedo': "",
            'monthly_avg_daily_horizontal_irradiance': "kWh/m2/giorno",
            'monthly_avg_daily_diffuse_horizontal_irradiance': "kWh/m2/giorno",
            'monthly_avg_daily_beam_horizontal_irradiance': "kWh/m2/giorno"
        }.items():
            if not self.validate_input(the_key, the_type):
                return False
        return True

    def compute(self):
        albedo = self.input['albedo'].value
        monthly_avg_daily_horizontal_irradiance = self.input['monthly_avg_daily_horizontal_irradiance']
        self.output['monthly_avg_daily_horizontal_irradiance'] = self.input['monthly_avg_daily_horizontal_irradiance']
        self.output['monthly_avg_daily_diffuse_horizontal_irradiance'] = (
            self.input['monthly_avg_daily_diffuse_horizontal_irradiance'])
        self.output['monthly_avg_daily_beam_horizontal_irradiance'] = (
            self.input['monthly_avg_daily_beam_horizontal_irradiance'])
        self.output['monthly_avg_daily_reflected_horizontal_irradiance']={}
        for month in months:
            horizontal_irradiance = monthly_avg_daily_horizontal_irradiance[month].value
            reflected_solar_radiation = round(horizontal_irradiance * albedo, 2)
            self.output['monthly_avg_daily_reflected_horizontal_irradiance'][month] = (
                Measure("kWh/m2/giorno", reflected_solar_radiation))


if __name__ == '__main__':
    the_target = MonthlyAvgDailyHorizontalSolarIrradianceSummary({
        "albedo": Measure("", 0.2),
        "monthly_avg_daily_horizontal_irradiance": {
            'GEN': Measure('kWh/m2', 1.14),
            'FEB': Measure('kWh/m2', 2.25),
            'MAR': Measure('kWh/m2', 3.47),
            'APR': Measure('kWh/m2', 4.2),
            'MAG': Measure('kWh/m2', 5.5),
            'GIU': Measure('kWh/m2', 6.25),
            'LUG': Measure('kWh/m2', 6.28),
            'AGO': Measure('kWh/m2', 5.25),
            'SET': Measure('kWh/m2', 3.84),
            'OTT': Measure('kWh/m2', 2.39),
            'NOV': Measure('kWh/m2', 1.3),
            'DIC': Measure('kWh/m2', 1.19)
        },
        "monthly_avg_daily_diffuse_horizontal_irradiance": {
            'GEN': Measure('kWh/m2', 0.58),
            'FEB': Measure('kWh/m2', 0.86),
            'MAR': Measure('kWh/m2', 1.22),
            'APR': Measure('kWh/m2', 1.81),
            'MAG': Measure('kWh/m2', 2.47),
            'GIU': Measure('kWh/m2', 2.69),
            'LUG': Measure('kWh/m2', 2.47),
            'AGO': Measure('kWh/m2', 2.39),
            'SET': Measure('kWh/m2', 1.78),
            'OTT': Measure('kWh/m2', 1.11),
            'NOV': Measure('kWh/m2', 0.61),
            'DIC': Measure('kWh/m2', 0.5)
        },
        "monthly_avg_daily_beam_horizontal_irradiance": {
            'GEN': Measure('kWh/m2', 0.56),
            'FEB': Measure('kWh/m2', 1.39),
            'MAR': Measure('kWh/m2', 2.25),
            'APR': Measure('kWh/m2', 2.39),
            'MAG': Measure('kWh/m2', 3.03),
            'GIU': Measure('kWh/m2', 3.56),
            'LUG': Measure('kWh/m2', 3.81),
            'AGO': Measure('kWh/m2', 2.86),
            'SET': Measure('kWh/m2', 2.06),
            'OTT': Measure('kWh/m2', 1.28),
            'NOV': Measure('kWh/m2', 0.69),
            'DIC': Measure('kWh/m2', 0.69)
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.get_output(True))
    else:
        print("input not valid, error")
        print(the_target.dump())
