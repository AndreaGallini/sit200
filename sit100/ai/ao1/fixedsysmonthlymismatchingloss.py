# arancione ITE 5 perdite per mismatching
from .concept import Measure, MeasureDerivation, months
from .utils import log, proper_round


class FixedSysMonthlyMismatchingLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {}
        except KeyError:
            log("error", "missing input data")
        self.output = {"fixed_sys_monthly_mismatching_loss": {mese: Measure("%", 2.0) for mese in months}}

    def validate(self):
        return True

    def compute(self):
        pass


if __name__ == '__main__':
    the_target = FixedSysMonthlyMismatchingLoss({})
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
