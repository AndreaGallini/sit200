# arancione ITE 2 perdite riflessione
from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyReflectionLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.input = the_input_data
        self.output = {"fixed_sys_monthly_reflection_loss": {mese: Measure("%", 3.0) for mese in months}}

    def validate(self):
        return True

    def compute(self):
        pass


if __name__ == '__main__':
    the_target = FixedSysMonthlyReflectionLoss({})
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
