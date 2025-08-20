# arancione ITE 1c perdite per temperatura formula empirica sistema fisso
from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyEmpiricalTempLoss(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        # TODO: spostare il db temperature (da norma) in un file JSON
        self.monthly_avg_temp = {
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
        self.output = {"fixed_sys_empirical_temp_loss": {mese: Measure("%/°C", 0.0) for mese in months}}

    def validate(self):
        return True

    def compute(self):
        total_temp = sum(self.monthly_avg_temp[month].value for month in months)
        annual_avg_temp = total_temp / len(months)
        for month in months:
            temp_loss_value = 4+(annual_avg_temp-11)/2
            rounded_temp_loss_value = round(temp_loss_value, 2)
            self.output["fixed_sys_empirical_temp_loss"][month] = Measure("%/°C", rounded_temp_loss_value)


if __name__ == '__main__':
    the_target = FixedSysMonthlyEmpiricalTempLoss({
        'monthly_avg_temp': {
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
