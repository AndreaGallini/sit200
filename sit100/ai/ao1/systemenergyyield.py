# RED E3E  system energy yield

from concept import Measure, MeasureDerivation
import utils


class SystemEnergyYield(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "peak_power": the_input_data["peak_power"].value,
                "annual_average_solar_radiation": the_input_data["annual_average_solar_radiation"].value,
                "module_efficiency": the_input_data["module_efficiency"].value/100,
                "inverter_efficiency": the_input_data["inverter_efficiency"].value/100,
                "system_losses": the_input_data["system_losses"].value/100,
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "system_energy_yield": None
        }

    def compute(self):
        annual_average_solar_radiation = self.input["annual_average_solar_radiation"]
        system_losses = self.input["system_losses"]
        usable_radiation = annual_average_solar_radiation * (1 - system_losses)
        peak_power = self.input["peak_power"]
        module_efficiency = self.input["module_efficiency"]
        module_energy_yield = peak_power * usable_radiation * module_efficiency
        inverter_efficiency = self.input["inverter_efficiency"]
        inverter_energy_yield = module_energy_yield * inverter_efficiency
        self.output["system_energy_yield"] = inverter_energy_yield


if __name__ == '__main__':
    the_target = SystemEnergyYield(
        {
            "peak_power": Measure("kW", 5.0),
            "annual_average_solar_radiation": Measure("kWh/m2/year", 1600.0),
            "module_efficiency": Measure("%", 18.0),
            "inverter_efficiency": Measure("%", 95.0),
            "system_losses": Measure("%", 10.0),
        }
    )
    the_target.main()
    print(the_target.dump())
