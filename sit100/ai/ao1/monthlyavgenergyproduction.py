# arancione EE 9 produzione media mensile
from .concept import Measure, MeasureDerivation, months


class MonthlyAvgEnergyProduction(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_energy_yield': the_input_data['monthly_energy_yield'],
                'nominal_peak_power': the_input_data['nominal_peak_power']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "monthly_avg_energy_production": {}
        }

    def validate(self):
        if not isinstance(self.input['nominal_peak_power'], Measure):
            print("Invalid input for nominal_peak_power: not a Measure")
            return False
        if self.input['nominal_peak_power'].unit != "kWp":
            print("Invalid input for nominal_peak_power: wrong unit")
            return False
        if not isinstance(self.input['monthly_energy_yield'], dict):
            print("Invalid input for monthly_energy_yield: not a dictionary")
            return False
        for month in months:
            if month not in self.input['monthly_energy_yield']:
                print(f"Missing measure for {month} in monthly_energy_yield")
                return False
            if not isinstance(self.input['monthly_energy_yield'][month], Measure):
                print(f"Invalid measure value for {month} in monthly_energy_yield: not a Measure")
                return False
            if self.input['monthly_energy_yield'][month].unit != "kWh/kWp":
                print(f"Invalid measure value for {month} in monthly_energy_yield: wrong unit")
                return False
        return True

    def compute(self):
        energy_yield = self.input['monthly_energy_yield']
        nominal_peak_power = self.input['nominal_peak_power'].value
        for month in months:
            monthly_energy_yield = energy_yield[month].value
            monthly_energy_production = round(monthly_energy_yield * nominal_peak_power, 2)
            self.output["monthly_avg_energy_production"][month] = Measure("kWh", monthly_energy_production)


if __name__ == '__main__':
    the_target = MonthlyAvgEnergyProduction({
        "monthly_energy_yield": {
            "GEN": Measure("kWh/kWp", 150.0),
            "FEB": Measure("kWh/kWp", 210.0),
            "MAR": Measure("kWh/kWp", 330.0),
            "APR": Measure("kWh/kWp", 420.0),
            "MAG": Measure("kWh/kWp", 480.0),
            "GIU": Measure("kWh/kWp", 510.0),
            "LUG": Measure("kWh/kWp", 540.0),
            "AGO": Measure("kWh/kWp", 450.0),
            "SET": Measure("kWh/kWp", 360.0),
            "OTT": Measure("kWh/kWp", 270.0),
            "NOV": Measure("kWh/kWp", 180.0),
            "DIC": Measure("kWh/kWp", 120.0)
        },
        "nominal_peak_power": Measure("kWp", 2.5)
    }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
