# Black Modello B3 Compatibilità della Potenza generatore vs. Potenza inverter
# in: inverter_max_power, generator_peak_power
# out: inverter_generator_power_ratio, inverter_generator_power_compatibility

from concept import Measure, MeasureDerivation
import utils


class InverterGeneratorPowerCompatibility(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                "inverter_max_power": the_input_data["inverter_max_power"],
                "generator_peak_power": the_input_data["generator_peak_power"]
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "inverter_generator_power_ratio": Measure("", 0.0),
            "inverter_generator_power_compatibility": Measure("bool", 0.0),
        }

    def validate(self):
        if not isinstance(self.input["inverter_max_power"], Measure):
            return False
        if not isinstance(self.input["inverter_max_power"].value, (int, float)):
            return False
        if not isinstance(self.input["generator_peak_power"], Measure):
            return False
        if not isinstance(self.input["generator_peak_power"].value, (int,float)):
            return False
        return True

    def compute(self):
        inverter_max_power = self.input["inverter_max_power"].value
        generator_peak_power = self.input["generator_peak_power"].value
        inverter_generator_power_ratio = tools.proper_round(inverter_max_power / 1000 / generator_peak_power, 2)
        self.output["inverter_generator_power_ratio"] = Measure("", inverter_generator_power_ratio)
        inverter_generator_power_compatibility = 0.78 < inverter_generator_power_ratio < 1.15
        self.output["inverter_generator_power_compatibility"] = Measure("bool", inverter_generator_power_compatibility)


if __name__ == '__main__':
    the_target = InverterGeneratorPowerCompatibility(
        {
            "inverter_max_power": Measure("W", 10000.00),
            "generator_peak_power": Measure("kW", 10.71),
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("error")
        print(the_target.dump())