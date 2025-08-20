# arancione ITE 10 perdita mensile da ombreggiamento

from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyShadingLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "fixed_sys_monthly_shading_loss_percentage": the_input_data["fixed_sys_monthly_shading_loss_percentage"],
                "monthly_plane_of_array_irradiance": the_input_data["monthly_plane_of_array_irradiance"]
            }
        except KeyError:
            log("ERROR", "FixedSysMonthlyShadingLoss: missing input data")
        self.output = {
            "fixed_sys_monthly_shading_loss": {mont: Measure("kWh/mq", 0.0) for mont in months}
        }

    def validate(self):
        for parameter in ['fixed_sys_monthly_shading_loss_percentage', 'monthly_plane_of_array_irradiance']:
            if parameter not in self.input:
                log("ERROR", f"FixedSysMonthlyShadingLoss: '{parameter}' key missing in input data")
                return False
            if not isinstance(self.input[parameter], dict):
                log("ERROR", f"FixedSysMonthlyShadingLoss: '{parameter}' input data must be dict")
                return False
            for month in months:
                if month not in self.input[parameter]:
                    log("ERROR", f"FixedSysMonthlyShadingLoss: '{parameter}' key {month} missing in input data")
                    return False
                if not isinstance(self.input[parameter][month], Measure):
                    log("ERROR",
                        f"FixedSysMonthlyShadingLoss: '{parameter}' on month {month} input data must be Measure")
                    return False
        return True

    def compute(self):
        for month in months:
            fixed_sys_monthly_shading_loss_percentage = self.input["fixed_sys_monthly_shading_loss_percentage"][month].value
            monthly_plane_of_array_irradiance = self.input["monthly_plane_of_array_irradiance"][month].value
            fixed_sys_monthly_shading_loss = round(fixed_sys_monthly_shading_loss_percentage * monthly_plane_of_array_irradiance / 100.0, 2)
            self.output["fixed_sys_monthly_shading_loss"][month] = Measure("kWh/mq", fixed_sys_monthly_shading_loss)


if __name__ == '__main__':
    the_target = FixedSysMonthlyShadingLoss({
        "fixed_sys_monthly_shading_loss_percentage": {
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
        "monthly_plane_of_array_irradiance": {
            "GEN": Measure("kWh/mq", 198.0),
            "FEB": Measure("kWh/mq", 182.0),
            "MAR": Measure("kWh/mq", 170.0),
            "APR": Measure("kWh/mq", 212.0),
            "MAG": Measure("kWh/mq", 121.0),
            "GIU": Measure("kWh/mq", 216.0),
            "LUG": Measure("kWh/mq", 211.0),
            "AGO": Measure("kWh/mq", 173.0),
            "SET": Measure("kWh/mq", 292.0),
            "OTT": Measure("kWh/mq", 111.0),
            "NOV": Measure("kWh/mq", 215.0),
            "DIC": Measure("kWh/mq", 119.0)
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
