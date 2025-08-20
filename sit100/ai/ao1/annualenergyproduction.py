# arancione EE 10 produzione energetica annua
from .concept import Measure, MeasureDerivation, months


class AnnualEnergyProduction(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_avg_energy_production': the_input_data['monthly_avg_energy_production']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "annual_energy_production": Measure("kWh", 1250.0)
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
                the_unit = value[month].unit
                if the_unit != 'kWh/mese' and the_unit != "kWh":
                    print(f"Invalid measure unit for {month} in {key}. Expected kWh/mese or kWh. Got {value[month].unit}")
                    return False
        return True

    def compute(self):
        monthly_avg_energy_production = self.input['monthly_avg_energy_production']
        annual_energy_production = 0
        for month in months:
            annual_energy_production += monthly_avg_energy_production[month].value
        self.output["annual_energy_production"] = Measure("kWh/anno", round(annual_energy_production,2))


if __name__ == '__main__':
    the_target = AnnualEnergyProduction({
        "monthly_avg_energy_production": {
            "GEN": Measure("kWh/mese", 375.0),
            "FEB": Measure("kWh/mese", 525.0),
            "MAR": Measure("kWh/mese", 825.0),
            "APR": Measure("kWh/mese", 1050.0),
            "MAG": Measure("kWh/mese", 1200.0),
            "GIU": Measure("kWh/mese", 1275.0),
            "LUG": Measure("kWh/mese", 1350.0),
            "AGO": Measure("kWh/mese", 1125.0),
            "SET": Measure("kWh/mese", 900.0),
            "OTT": Measure("kWh/mese", 675.0),
            "NOV": Measure("kWh/mese", 450.0),
            "DIC": Measure("kWh/mese", 300.0)
        }
    }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
