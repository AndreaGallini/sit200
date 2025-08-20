# arancione ITE 1a perdite per temperatura sistema fisso
from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyTempLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "monthly_avg_daily_temperature": the_input_data["monthly_avg_daily_temperature"]
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {"fixed_sys_monthly_temp_loss": {mese: Measure("%", 0.0) for mese in months}}

    def validate(self):
        if "monthly_avg_daily_temperature" not in self.input:
            log("ERROR", "FixedSysMonthlyTempLoss: monthly average temperature not given")
        if not isinstance(self.input["monthly_avg_daily_temperature"], dict):
            log("ERROR", "FixedSysMonthlyTempLoss: monthly average temperature wrong type")
        if not len(self.input["monthly_avg_daily_temperature"]) == 12:
            log("ERROR", "FixedSysMonthlyTempLoss: monthly average temperature wrong length")
        for month in months:
            if month not in self.input["monthly_avg_daily_temperature"]:
                log("ERROR", "FixedSysMonthlyTempLoss: missing monthly average temperature")
            if not isinstance(self.input["monthly_avg_daily_temperature"][month], Measure):
                log("ERROR", "FixedSysMonthlyTempLoss: monthly average temperature wrong type")
        return True

    def compute(self):
        coeff = -0.4  # %/C°
        for month in months:
            temp = self.input["monthly_avg_daily_temperature"][month].value
            temp_loss_value = (4+(temp-13)/2) * coeff / -0.4
            rounded_temp_loss_value = round(temp_loss_value, 2)
            self.output["fixed_sys_monthly_temp_loss"][month] = Measure("%", rounded_temp_loss_value)


if __name__ == '__main__':
    the_target = FixedSysMonthlyTempLoss({
        'monthly_avg_daily_temperature': {
            "GEN": Measure("°C", 3.3),
            "FEB": Measure("°C", 4.8),
            "MAR": Measure("°C", 8.6),
            "APR": Measure("°C", 13.2),
            "MAG": Measure("°C", 17.3),
            "GIU": Measure("°C", 21.3),
            "LUG": Measure("°C", 23.6),
            "AGO": Measure("°C", 23.4),
            "SET": Measure("°C", 20.4),
            "OTT": Measure("°C", 14.9),
            "NOV": Measure("°C", 9.5),
            "DIC": Measure("°C", 5.0)
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
