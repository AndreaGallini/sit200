# arancione EE 5 producibilità annua
from .concept import Measure, MeasureDerivation, months


class AnnualEnergyYield(MeasureDerivation):
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
            "annual_energy_yield": Measure("kWh/kWp", 0.0)
        }

    def validate(self):
        for key, value in self.input.items():
            if not isinstance(value, dict):
                print(f"Invalid input for {key}: not a dictionary")
                return False
            for month in months:
                if month not in value:
                    print(f"Missing measure for {month} in {key}")
                    return False
                if not isinstance(value[month], Measure):
                    print(f"Invalid measure value for {month} in {key}: not a Measure")
                    return False
        return True

    def compute(self):
        monthly_energy_yield = self.input['monthly_energy_yield']
        annual_energy_yield = 0
        for month in months:
            annual_energy_yield += monthly_energy_yield[month].value
        self.output["annual_energy_yield"] = Measure("kWh/kWp", round(annual_energy_yield, 2))


if __name__ == '__main__':
    the_target = AnnualEnergyYield({
        "monthly_energy_yield": {
            "GEN": Measure("kWh/kWp/mese", 50.0),
            "FEB": Measure("kWh/kWp/mese", 70.0),
            "MAR": Measure("kWh/kWp/mese", 110.0),
            "APR": Measure("kWh/kWp/mese", 140.0),
            "MAG": Measure("kWh/kWp/mese", 160.0),
            "GIU": Measure("kWh/kWp/mese", 170.0),
            "LUG": Measure("kWh/kWp/mese", 180.0),
            "AGO": Measure("kWh/kWp/mese", 150.0),
            "SET": Measure("kWh/kWp/mese", 120.0),
            "OTT": Measure("kWh/kWp/mese", 90.0),
            "NOV": Measure("kWh/kWp/mese", 60.0),
            "DIC": Measure("kWh/kWp/mese", 40.0)
        }
    }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
