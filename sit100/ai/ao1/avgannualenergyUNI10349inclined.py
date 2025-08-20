# RED E2E  Average annual energy UNI 10349 inclined plane

from concept import Measure, MeasureDerivation
import csv
import utils


class AvgAnnualEnergyUNI10349Inclined(MeasureDerivation):
    def __init__(self, data_file_name, the_input_data=None):
        self.inclined_annual_solar_radiations = {}
        self.load_data(data_file_name)
        super().__init__()
        try:
            self.input = {
                "avg_annual_energy_uni10349_horizontal": the_input_data['avg_annual_energy_uni10349_horizontal'],
                "zone": the_input_data['zone'],
                "orientation": the_input_data['orientation'],
                "tilt": the_input_data['tilt'],
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "avg_annual_energy_uni10349_inclined": None
        }

    def load_data(self, filename):
        try:
            super().load_data(filename)
        except FileNotFoundError:
            print("File not found")
            quit()
        with open(filename, newline='') as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                try:
                    zona, tilt, orientation, value_str = row
                    value = float(value_str)
                    self.inclined_annual_solar_radiations[(zona, tilt, orientation)] = value
                except (ValueError, IndexError) as e:
                    print(f"Error on row: {row}. {e}")

    def compute(self):
        zone = self.input['zone']
        orientation = self.input["orientation"]
        tilt = self.input["tilt"]
        try:
            inclined_annual_solar_radiation = self.inclined_annual_solar_radiations[(zone, tilt, orientation)]
        except (ValueError, KeyError) as e:
            print("Error on zone, tilt, orientation", zone, tilt, orientation)
            print(self.inclined_annual_solar_radiations)
            quit()
        avg_annual_energy_uni10349_horizontal = self.input["avg_annual_energy_uni10349_horizontal"]
        avg_annual_energy_uni10349_inclined = inclined_annual_solar_radiation * avg_annual_energy_uni10349_horizontal
        self.output['avg_annual_energy_uni10349_inclined'] = tools.proper_round(avg_annual_energy_uni10349_inclined)


if __name__ == '__main__':
    the_target = AvgAnnualEnergyUNI10349Inclined(
        "inclined_annual_solar_radiations.csv",
        {
            "zone": "Centro Italia",
            "orientation": '30',
            "tilt": '30',
            "avg_annual_energy_uni10349_horizontal": 3107.25
        }
    )
    the_target.main()
    print(the_target.dump())
