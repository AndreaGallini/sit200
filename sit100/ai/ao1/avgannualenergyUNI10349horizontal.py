# RED E1E Average annual energy UNI 10349 Horizontal

from concept import Measure, MeasureDerivation


class AvgAnnualEnergyUNI10349Horizontal(MeasureDerivation):
    def __init__(self, data_file_name, the_input_data=None):
        self.horizontal_annual_solar_radiations = {}
        self.load_data(data_file_name)
        super().__init__()
        try:
            self.input = {
                "site": the_input_data['site'],
                "system_power": the_input_data['system_power'],
                "system_efficiency": the_input_data['system_efficiency'],
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "avg_annual_energy_uni10349": None
        }

    def load_data(self, filename):
        try:
            super().load_data(filename)
        except FileNotFoundError:
            print("File not found")
            quit()
        with open(filename, mode='r') as file:
            next(file)
            for line in file:
                try:
                    site, value = line.split(";")
                    self.horizontal_annual_solar_radiations[site] = float(value)
                except ValueError:
                    print("invalid file format")
                    quit()

    def compute(self):
        horizontal_annual_solar_radiation = self.horizontal_annual_solar_radiations[self.input["site"]]
        system_power = self.input["system_power"].get_value()
        system_efficiency = self.input["system_efficiency"]
        avg_annual_energy_uni10349 = horizontal_annual_solar_radiation * system_power * system_efficiency
        self.output['avg_annual_energy_uni10349'] = avg_annual_energy_uni10349


if __name__ == '__main__':
    the_target = AvgAnnualEnergyUNI10349Horizontal(
        "horizontal_annual_solar_radiations.csv",
        {
            "site": "L'Aquila",
            "system_power": Measure("kW", 3),
            "system_efficiency": 0.75
        }
    )
    the_target.main()
    print(the_target.dump())
