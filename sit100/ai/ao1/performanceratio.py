# RED E7E performance ratio
import utils
from concept import Measure, MeasureDerivation
import os.path
import matplotlib.pyplot as plt


class PerformanceRatio(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "nominal_power": the_input_data["nominal_power"],
                "monthly_incident_solar_radiation": the_input_data["monthly_incident_solar_radiation"],
                "actual_energy_production": the_input_data["actual_energy_production"],
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "performance_ratio": None
        }

    def compute(self):
        nominal_power = self.input["nominal_power"].value
        monthly_incident_solar_radiation = self.input["monthly_incident_solar_radiation"].value
        actual_energy_production = self.input["actual_energy_production"].value
        performance_ratio = actual_energy_production / (nominal_power * monthly_incident_solar_radiation)
        self.output["performance_ratio"] = Measure("%", tools.proper_round(performance_ratio * 100))


if __name__ == '__main__':
    the_target = PerformanceRatio(
        {
            "nominal_power": Measure("kW", 3.0),
            "monthly_incident_solar_radiation": Measure("kWh/m2", 150.0),
            "actual_energy_production": Measure("kWh", 380.0),
        }
    )
    the_target.main()
    print(the_target.dump())
