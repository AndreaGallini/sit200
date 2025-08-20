# arancione ITE 7 perdite inverter
from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyInverterLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {"european_inverter_efficiency": the_input_data["european_inverter_efficiency"]}
        except KeyError:
            log("error", "missing input data")
        self.output = {"fixed_sys_monthly_inverter_loss": {mese: Measure("%", 0.0) for mese in months}}

    def validate(self):
        return True

    def compute(self):
        european_inverter_efficiency = self.input['european_inverter_efficiency'].value
        fixed_sys_monthly_inverter_loss = 100.0 - european_inverter_efficiency
        self.output = {"fixed_sys_monthly_inverter_loss": {
            mese: Measure("%", fixed_sys_monthly_inverter_loss) for mese in months
        }}


if __name__ == '__main__':
    the_target = FixedSysMonthlyInverterLoss({
        "european_inverter_efficiency": Measure("%", 94.0)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
