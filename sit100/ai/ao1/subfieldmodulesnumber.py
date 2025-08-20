# RED E10E Energy Self-Sufficiency Factor
# in: strings_per_subfield, modules_per_subfield_string
# out: total_modules

from concept import Measure, MeasureDerivation
import utils


class SubFieldModulesNumber(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                "strings_per_subfield": the_input_data["strings_per_subfield"],
                "modules_per_subfield_string": the_input_data["modules_per_subfield_string"]
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "total_modules": Measure("", 0.0),
        }

    def validate(self):
        if not isinstance(self.input["modules_per_subfield_string"], list):
            return False
        for module in self.input["modules_per_subfield_string"]:
            if not isinstance(module, Measure):
                return False
            if not isinstance(module.value, (int, float)):
                return False
        if not isinstance(self.input["strings_per_subfield"], list):
            return False
        if len(self.input["strings_per_subfield"]) != len(self.input["modules_per_subfield_string"]):
            return False
        return True

    def compute(self):
        total_modules_number = 0
        for i, modules_number in enumerate(self.input["modules_per_subfield_string"]):
            n = modules_number.value * self.input["strings_per_subfield"][i].value
            total_modules_number += n
        self.output["total_modules"] = Measure("", total_modules_number)


if __name__ == '__main__':
    the_target = SubFieldModulesNumber(
        {
            "strings_per_subfield": [
                Measure("", 2.0),
                Measure("", 5.0),
                Measure("", 7.0),
                Measure("", 3.0)
            ],
            "modules_per_subfield_string": [
                Measure("", 20.0),
                Measure("", 10.0),
                Measure("", 30.0),
                Measure("", 10.0),
            ]
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("error")
        print(the_target.dump())