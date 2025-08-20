# arancione ITE 3 perdite per sporcamento
from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlySoilingLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "tilt": the_input_data["tilt"]
            }
        except KeyError:
            log("error", "missing input data")
        self.output = {"fixed_sys_monthly_soiling_loss": {mese: Measure("%", 0.0) for mese in months}}

    def validate(self):
        if not isinstance(self.input["tilt"], Measure):
            log("error", "tilt value must be a Measure object")
            return False
        if not self.input["tilt"].value:
            log("error", "missing tilt value")
            return False
        if not isinstance(self.input["tilt"].value, (int, float)):
            log("error", "tilt value must be a number")
            return False
        return True

    def compute(self):
        for mese in months:
            tilt = self.input["tilt"].value
            soiling_loss_value = max(1.0, (12-tilt)/2)
            self.output["fixed_sys_monthly_soiling_loss"][mese] = Measure("%", soiling_loss_value)


if __name__ == '__main__':
    the_target = FixedSysMonthlySoilingLoss({
        "tilt": Measure("°", 9)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
