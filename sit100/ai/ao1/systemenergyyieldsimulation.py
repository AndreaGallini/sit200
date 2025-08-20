# RED E5E system energy yield simulation
import utils
from concept import Measure, MeasureDerivation


class SystemEnergyYieldSimulation(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "peak_power": the_input_data["peak_power"],
                "modules_efficiency": the_input_data["modules_efficiency"],
                "modules_number": the_input_data["modules_number"],
                "inverter_efficiency":the_input_data["inverter_efficiency"],
                "annual_average_solar_radiation": the_input_data["annual_average_solar_radiation"],
                "annual_average_temperature": the_input_data["annual_average_temperature"],
                "annual_sunshine_hours": the_input_data["annual_sunshine_hours"],
                "tilt": the_input_data["tilt"],
                "orientation": the_input_data["orientation"],
                "system_losses": the_input_data["system_losses"],
                "temperature_coefficient": the_input_data["temperature_coefficient"],
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "system_energy_yield": None
        }

    def compute(self):
        peak_power = self.input["peak_power"].value
        modules_efficiency = self.input["modules_efficiency"].value / 100
        modules_number = self.input["modules_number"].value
        inverter_efficiency = self.input["inverter_efficiency"].value / 100
        annual_average_solar_radiation = self.input["annual_average_solar_radiation"].value
        annual_average_temperature = self.input["annual_average_temperature"].value
        annual_sunshine_hours = self.input["annual_sunshine_hours"].value
        tilt = self.input["tilt"].value
        orientation = self.input["orientation"].value
        system_losses = self.input["system_losses"].value / 100
        temperature_coefficient = self.input["temperature_coefficient"].value / 100
        usable_radiation = annual_average_solar_radiation * (1-system_losses)
        theoretical_modules_energy_yield = peak_power * usable_radiation
        module_efficiency_by_temperature = (
                modules_efficiency
                * (1+temperature_coefficient*(annual_average_temperature-25))
        )
        module_energy_yield = peak_power * annual_sunshine_hours * module_efficiency_by_temperature
        system_energy_yield = module_energy_yield * inverter_efficiency
        self.output["system_energy_yield"] = tools.proper_round(system_energy_yield)


if __name__ == '__main__':
    the_target = SystemEnergyYieldSimulation(
        {
            "peak_power": Measure("kWh", 10.0),
            "modules_efficiency": Measure("%", 20.0),
            "modules_number": Measure("", 40.0),
            "inverter_efficiency": Measure("%", 97.0),
            "annual_average_solar_radiation": Measure("kWh/m2/year", 1700.0),
            "annual_average_temperature": Measure("°C", 16.0),
            "annual_sunshine_hours": Measure("", 1800.0),
            "tilt": Measure("°", 30.0),
            "orientation": Measure("°", 0.0),
            "system_losses": Measure("%", 10.0),
            "temperature_coefficient": Measure("°C%", -0.4)
        }
    )
    the_target.main()
    print(the_target.dump())
