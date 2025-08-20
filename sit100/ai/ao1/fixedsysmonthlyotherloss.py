# arancione ITE 5 perdite per mismatching
from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyOtherLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.output = {"fixed_sys_monthly_other_loss": {month: Measure("%", 0.0) for month in months}}

    def validate(self):
        return True

    def compute(self):
        self.output = {"fixed_sys_monthly_other_loss": {month: Measure("%", 1.0) for month in months}}


if __name__ == '__main__':
    the_target = FixedSysMonthlyOtherLoss()
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
