# arancione ITE 6 perdite per cavi
from .concept import Measure, MeasureDerivation, months
from .utils import log, proper_round


class FixedSysMonthlyCableLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.output = {"fixed_sys_monthly_cable_loss": {month: Measure("%", 0.0) for month in months}}

    def validate(self):
        return True

    def compute(self):
        nominal_loss_value = 1.0
        fixed_sys_monthly_cable_loss_value = nominal_loss_value * 2/3
        rounded_fixed_sys_monthly_cable_loss_value = proper_round(fixed_sys_monthly_cable_loss_value, 2)
        for month in months:
            self.output["fixed_sys_monthly_cable_loss"][month] = Measure("%", rounded_fixed_sys_monthly_cable_loss_value)


if __name__ == '__main__':
    the_target = FixedSysMonthlyCableLoss({})
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
