# RED E4E  system energy yield base formula

from concept import Measure, MeasureDerivation


class SystemEnergyYieldBaseFormula(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "peak_power": the_input_data["peak_power"].value,
                "annual_effective_sunshine_hours": the_input_data["annual_effective_sunshine_hours"].value,
                "system_efficiency": the_input_data["system_efficiency"].value/100,
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "system_energy_yield_base_formula": None
        }

    def compute(self):
        peak_power = self.input["peak_power"]
        annual_effective_sunshine_hours = self.input["annual_effective_sunshine_hours"]
        system_efficiency = self.input["system_efficiency"]
        system_energy_yield_base_formula = peak_power * annual_effective_sunshine_hours * system_efficiency
        self.output["system_energy_yield_base_formula"] = system_energy_yield_base_formula


if __name__ == '__main__':
    the_target = SystemEnergyYieldBaseFormula(
        {
            "peak_power": Measure("kW", 5.0),
            "annual_effective_sunshine_hours": Measure("H/year", 1600.0),
            "system_efficiency": Measure("%", 85.0)
        }
    )
    the_target.main()
    print(the_target.dump())
