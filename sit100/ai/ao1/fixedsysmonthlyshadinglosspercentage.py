# arancione ITE 9f perdita mensile percentuale da ombreggiamento

from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyShadingLossPercentage(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "fixed_sys_monthly_obstacle_shading": the_input_data["fixed_sys_monthly_obstacle_shading"],
                "fixed_sys_monthly_clinometric_shading": the_input_data["fixed_sys_monthly_clinometric_shading"]
            }
        except KeyError:
            log("ERROR", "FixedSysMonthlyShadingLossPercentage: missing input data")
        self.output = {
            "fixed_sys_monthly_shading_loss_percentage": {mont: Measure("%", 0.0) for mont in months}
        }

    def validate(self):
        for parameter in ['fixed_sys_monthly_obstacle_shading', 'fixed_sys_monthly_clinometric_shading']:
            if parameter not in self.input:
                log("ERROR", f"FixedSysMonthlyShadingLossPercentage: '{parameter}' key missing in input data")
                return False
            if not isinstance(self.input[parameter], dict):
                log("ERROR", f"FixedSysMonthlyShadingLossPercentage: '{parameter}' input data must be dict")
                return False
            for month in months:
                if month not in self.input[parameter]:
                    log("ERROR", f"FixedSysMonthlyShadingLossPercentage: '{parameter}' key {month} missing in input data")
                    return False
                if not isinstance(self.input[parameter][month], Measure):
                    log("ERROR",
                        f"FixedSysMonthlyShadingLossPercentage: '{parameter}' on month {month} input data must be Measure")
                    return False
        return True

    def compute(self):
        for month in months:
            fixed_sys_monthly_obstacle_shading = self.input["fixed_sys_monthly_obstacle_shading"][month].value
            fixed_sys_monthly_clinometric_shading = self.input["fixed_sys_monthly_clinometric_shading"][month].value
            the_sum = fixed_sys_monthly_obstacle_shading + fixed_sys_monthly_clinometric_shading
            the_max = max(fixed_sys_monthly_obstacle_shading, fixed_sys_monthly_clinometric_shading)
            the_mean = the_sum / 2.0
            the_min = 0
            fixed_sys_monthly_shading_loss_percentage = round((the_sum + the_max + the_mean + the_min) / 4.0, 2)
            self.output["fixed_sys_monthly_shading_loss_percentage"][month] = Measure("%", fixed_sys_monthly_shading_loss_percentage)


if __name__ == '__main__':
    the_target = FixedSysMonthlyShadingLossPercentage({
        "fixed_sys_monthly_obstacle_shading": {
            "GEN": Measure("%", 10.0),
            "FEB": Measure("%", 15.0),
            "MAR": Measure("%", 20.0),
            "APR": Measure("%", 25.0),
            "MAG": Measure("%", 20.0),
            "GIU": Measure("%", 15.0),
            "LUG": Measure("%", 10.0),
            "AGO": Measure("%", 5.0),
            "SET": Measure("%", 7.0),
            "OTT": Measure("%", 13.0),
            "NOV": Measure("%", 18.0),
            "DIC": Measure("%", 20.0)
        },
        "fixed_sys_monthly_clinometric_shading": {
            "GEN": Measure("%", 8.0),
            "FEB": Measure("%", 12.0),
            "MAR": Measure("%", 13.0),
            "APR": Measure("%", 22.0),
            "MAG": Measure("%", 21.0),
            "GIU": Measure("%", 16.0),
            "LUG": Measure("%", 11.0),
            "AGO": Measure("%", 7.0),
            "SET": Measure("%", 9.0),
            "OTT": Measure("%", 11.0),
            "NOV": Measure("%", 15.0),
            "DIC": Measure("%", 19.0)
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
