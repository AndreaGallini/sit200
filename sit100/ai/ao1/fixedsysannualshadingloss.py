# arancione ITE 11 perdita annuale da ombreggiamento

from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysAnnualShadingLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "fixed_sys_monthly_shading_loss": the_input_data["fixed_sys_monthly_shading_loss"]
            }
        except KeyError:
            log("ERROR", "FixedSysAnnualShadingLoss: missing input data")
        self.output = {
            "fixed_sys_annual_shading_loss": Measure("kWh/mq", 0.0)
        }

    def validate(self):
        for parameter in ['fixed_sys_monthly_shading_loss']:
            if parameter not in self.input:
                log("ERROR", f"FixedSysAnnualShadingLoss: '{parameter}' key missing in input data")
                return False
            if not isinstance(self.input[parameter], dict):
                log("ERROR", f"FixedSysAnnualShadingLoss: '{parameter}' input data must be dict")
                return False
            for month in months:
                if month not in self.input[parameter]:
                    log("ERROR", f"FixedSysAnnualShadingLoss: '{parameter}' key {month} missing in input data")
                    return False
                if not isinstance(self.input[parameter][month], Measure):
                    log("ERROR",
                        f"FixedSysAnnualShadingLoss: '{parameter}' on month {month} input data must be Measure")
                    return False
        return True

    def compute(self):
        fixed_sys_annual_shading_loss = 0
        for month in months:
            fixed_sys_monthly_shading_loss = self.input["fixed_sys_monthly_shading_loss"][month].value
            fixed_sys_annual_shading_loss += fixed_sys_monthly_shading_loss
        self.output["fixed_sys_annual_shading_loss"] = Measure("kWh/mq", round(fixed_sys_annual_shading_loss,2))


if __name__ == '__main__':
    the_target = FixedSysAnnualShadingLoss({
        "fixed_sys_monthly_shading_loss": {
            "GEN": Measure("kWh/mq", 19.0),
            "FEB": Measure("kWh/mq", 18.0),
            "MAR": Measure("kWh/mq", 17.0),
            "APR": Measure("kWh/mq", 21.0),
            "MAG": Measure("kWh/mq", 12.0),
            "GIU": Measure("kWh/mq", 21.0),
            "LUG": Measure("kWh/mq", 21.0),
            "AGO": Measure("kWh/mq", 17.0),
            "SET": Measure("kWh/mq", 29.0),
            "OTT": Measure("kWh/mq", 11.0),
            "NOV": Measure("kWh/mq", 21.0),
            "DIC": Measure("kWh/mq", 11.0)
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
