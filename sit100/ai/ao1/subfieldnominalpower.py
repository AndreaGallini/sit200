# Black Modello B2 peak power per subfield
# in: modules_per_subfield, module_peak_power
# out: peak_power_per_subfield, generator_peak_power

from concept import Measure, MeasureDerivation
import utils


class SubFieldNominalPower(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                "modules_per_subfield": the_input_data["modules_per_subfield"],
                "module_peak_power": the_input_data["module_peak_power"]
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "nominal_power": Measure("kW", 0.0),
            "nominal_power_per_subfield": []
        }

    def validate(self):
        if not isinstance(self.input["modules_per_subfield"], list):
            return False
        for module in self.input["modules_per_subfield"]:
            if not isinstance(module, Measure):
                return False
            if not isinstance(module.value, (int, float)):
                return False
        if not isinstance(self.input["module_peak_power"], Measure):
            return False
        if not isinstance(self.input["module_peak_power"].value, (int,float)):
            return False
        return True

    def compute(self):
        module_peak_power = self.input["module_peak_power"].value
        nominal_power = 0
        for modules_number in self.input["modules_per_subfield"]:
            subfield_nominal_power = modules_number.value * module_peak_power / 1000
            self.output["nominal_power_per_subfield"].append(Measure("kW", subfield_nominal_power))
            nominal_power += subfield_nominal_power
        self.output["nominal_power"] = Measure("kW", nominal_power)


if __name__ == '__main__':
    the_target = SubFieldNominalPower(
        {
            "modules_per_subfield": [
                Measure("", 40.0),
                Measure("", 50.0),
                Measure("", 210.0),
                Measure("", 30.0)
            ],
            "module_peak_power": Measure("W", 250.0)
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("error")
        print(the_target.dump())