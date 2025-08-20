# arancione ITE 4 perdite per bassi livelli di irraggiamento
from .concept import Measure, MeasureDerivation, months
from .utils import log, proper_round


class FixedSysMonthlyLowIrradianceLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "theoretical_annual_yield": the_input_data["theoretical_annual_yield"]
            }
        except KeyError:
            log("error", "missing input data")
        self.output = {"fixed_sys_monthly_low_irradiance_loss": {mese: Measure("%", 0.0) for mese in months}}

    def validate(self):
        if not isinstance(self.input["theoretical_annual_yield"], Measure):
            log("error", "theoretical annual yield value must be a Measure object")
            return False
        if not self.input["theoretical_annual_yield"].value:
            log("error", "missing theoretical annual yield value")
            return False
        if not isinstance(self.input["theoretical_annual_yield"].value, (int, float)):
            log("error", "theoretical annual yield value must be a number")
            return False
        return True

    def compute(self):
        for mese in months:
            theoretical_annual_yield = self.input["theoretical_annual_yield"].value
            low_irradiance_loss_value = proper_round(40.0/theoretical_annual_yield, 2)
            self.output["fixed_sys_monthly_low_irradiance_loss"][mese] = Measure("%", low_irradiance_loss_value)


if __name__ == '__main__':
    the_target = FixedSysMonthlyLowIrradianceLoss({
        "theoretical_annual_yield": Measure("kWh/kWp", 1500.0)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
