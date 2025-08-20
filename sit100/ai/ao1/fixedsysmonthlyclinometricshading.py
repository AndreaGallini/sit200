# arancione ITE 9e ombreggiamento clinometrico
from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyClinometricShading(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        if the_input_data is None:
            self.input = { "shading_horizon": Measure("%", 0.0)}
        else:
            try:
                self.input = {
                    "shading_horizon": the_input_data["shading_horizon"]
                    }
            except KeyError:
                log("ERROR", "clinometricShading: missing input data")
        self.output = {
            "fixed_sys_monthly_clinometric_shading": {month: Measure("%", 0.0) for month in months}
        }

    def validate(self):
        if "shading_horizon" not in self.input:
            log("ERROR", "FixedSysClinometricShading: 'shading_horizon' key missing in input data")
            return False

        shading_horizon = self.input["shading_horizon"]
        if not isinstance(shading_horizon, Measure):
            log("ERROR", "FixedSysClinometricShading: 'shading_horizon' should be a dictionary")
            return False

        if not isinstance(shading_horizon, Measure):
            log("ERROR", f"FixedSysClinometricShading: data is not a Measure")
            return False
        if not (0 <= shading_horizon.value <= 20):
            log("ERROR", f"FixedSysClinometricShading: value is out of range (0-25)")
            return False
        return True

    def compute(self):
        for month in months:
            self.output["fixed_sys_monthly_clinometric_shading"][month] = self.input["shading_horizon"]


if __name__ == '__main__':
    the_target = FixedSysMonthlyClinometricShading({"shading_horizon": Measure("%", 3.2)})
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
