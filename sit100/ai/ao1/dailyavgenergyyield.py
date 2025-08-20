# arancione EE 7 producibilità giornaliera media giorno
from .concept import Measure, MeasureDerivation, months


class DailyAvgEnergyYield(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_energy_yield': the_input_data['monthly_energy_yield']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "daily_avg_energy_yield": {month: Measure("%", 0.0) for month in months}
        }

    def validate(self):
        # controllare unità di misura e numerosità delle misure mensili di energia
        return True

    def compute(self):
        monthly_energy_yield = self.input['monthly_energy_yield']
        self.output['daily_avg_energy_yield'] = {}
        for month in monthly_energy_yield:
            days_in_month = months[month]
            daily_avg_energy_yield = round(monthly_energy_yield[month].value / days_in_month, 2)
            self.output['daily_avg_energy_yield'][month] = Measure("kWh/m2", daily_avg_energy_yield)


if __name__ == '__main__':
    the_target = DailyAvgEnergyYield({
        'monthly_energy_yield': {
            "GEN": Measure("kWh/kWp", 50.0),
            "FEB": Measure("kWh/kWp", 70.0),
            "MAR": Measure("kWh/kWp", 100.0),
            "APR": Measure("kWh/kWp", 130.0),
            "MAG": Measure("kWh/kWp", 150.0),
            "GIU": Measure("kWh/kWp", 140.0),
            "LUG": Measure("kWh/kWp", 130.0),
            "AGO": Measure("kWh/kWp", 110.0),
            "SET": Measure("kWh/kWp", 90.0),
            "OTT": Measure("kWh/kWp", 70.0),
            "NOV": Measure("kWh/kWp", 50.0),
            "DIC": Measure("kWh/kWp", 40.0),
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
