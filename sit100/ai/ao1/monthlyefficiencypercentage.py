# arancione EE 3 efficienza mensile percentuale
from .concept import Measure, MeasureDerivation, months


class MonthlyEfficiencyPercentage(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'fixed_sys_monthly_temp_loss': the_input_data['fixed_sys_monthly_temp_loss'],
                'fixed_sys_monthly_reflection_loss': the_input_data['fixed_sys_monthly_reflection_loss'],
                'fixed_sys_monthly_soiling_loss': the_input_data['fixed_sys_monthly_soiling_loss'],
                'fixed_sys_monthly_low_irradiance_loss': the_input_data['fixed_sys_monthly_low_irradiance_loss'],
                'fixed_sys_monthly_mismatching_loss': the_input_data['fixed_sys_monthly_mismatching_loss'],
                'fixed_sys_monthly_cable_loss': the_input_data['fixed_sys_monthly_cable_loss'],
                'fixed_sys_monthly_inverter_loss': the_input_data['fixed_sys_monthly_inverter_loss'],
                'fixed_sys_monthly_other_loss': the_input_data['fixed_sys_monthly_other_loss']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "monthly_efficiency_percentage": {month: Measure("%", 0.0) for month in months}
        }

    def validate(self):
        for key, monthly_values in self.input.items():
            if not isinstance(monthly_values, dict):
                print(f"Invalid input for {key}: not a dictionary")
                return False
            for month in months:
                if month not in monthly_values:
                    print(f"Missing measure for {month} in {key}")
                    return False
                if not isinstance(monthly_values[month], Measure):
                    print(f"Invalid measure value for {month} in {key}: not a Measure")
                    return False
                if not isinstance(monthly_values[month].value, (int, float)):
                    print(f"Invalid value for {month} in {key}: not a number")
                    return False
        return True

    def compute(self):
        monthly_efficiency = {}
        for month in months:
            efficiency_product = 1.0
            for key, monthly_values in self.input.items():
                the_value = monthly_values[month].value / 100.0
                efficiency_product *= 1.0 - the_value
            monthly_efficiency[month] = round(efficiency_product * 100.0, 2)
            self.output["monthly_efficiency_percentage"][month] = Measure("%", monthly_efficiency[month])


if __name__ == '__main__':
    the_target = MonthlyEfficiencyPercentage({
    "fixed_sys_monthly_temp_loss": {
        "GEN": Measure("%", 2.91),
        "FEB": Measure("%", 4.85),
        "MAR": Measure("%", 3.74),
        "APR": Measure("%", 1.97),
        "MAG": Measure("%", 4.65),
        "GIU": Measure("%", 4.33),
        "LUG": Measure("%", 2.84),
        "AGO": Measure("%", 4.13),
        "SET": Measure("%", 3.76),
        "OTT": Measure("%", 2.61),
        "NOV": Measure("%", 4.07),
        "DIC": Measure("%", 3.74)
    },
    "fixed_sys_monthly_reflection_loss": {
        "GEN": Measure("%", 2.16),
        "FEB": Measure("%", 2.49),
        "MAR": Measure("%", 2.24),
        "APR": Measure("%", 3.09),
        "MAG": Measure("%", 3.36),
        "GIU": Measure("%", 3.85),
        "LUG": Measure("%", 1.15),
        "AGO": Measure("%", 3.47),
        "SET": Measure("%", 2.35),
        "OTT": Measure("%", 4.97),
        "NOV": Measure("%", 1.54),
        "DIC": Measure("%", 2.53)
    },
    "fixed_sys_monthly_soiling_loss": {
        "GEN": Measure("%", 3.48),
        "FEB": Measure("%", 3.01),
        "MAR": Measure("%", 3.28),
        "APR": Measure("%", 4.72),
        "MAG": Measure("%", 2.19),
        "GIU": Measure("%", 1.72),
        "LUG": Measure("%", 3.66),
        "AGO": Measure("%", 2.95),
        "SET": Measure("%", 2.64),
        "OTT": Measure("%", 1.41),
        "NOV": Measure("%", 2.54),
        "DIC": Measure("%", 3.77)
    },
    "fixed_sys_monthly_low_irradiance_loss": {
        "GEN": Measure("%", 1.58),
        "FEB": Measure("%", 2.15),
        "MAR": Measure("%", 1.33),
        "APR": Measure("%", 4.24),
        "MAG": Measure("%", 4.28),
        "GIU": Measure("%", 1.35),
        "LUG": Measure("%", 1.31),
        "AGO": Measure("%", 2.83),
        "SET": Measure("%", 4.57),
        "OTT": Measure("%", 2.88),
        "NOV": Measure("%", 4.74),
        "DIC": Measure("%", 2.58)
    },
    "fixed_sys_monthly_mismatching_loss": {
        "GEN": Measure("%", 2.84),
        "FEB": Measure("%", 3.71),
        "MAR": Measure("%", 1.48),
        "APR": Measure("%", 3.10),
        "MAG": Measure("%", 3.83),
        "GIU": Measure("%", 2.32),
        "LUG": Measure("%", 2.18),
        "AGO": Measure("%", 1.42),
        "SET": Measure("%", 1.04),
        "OTT": Measure("%", 4.12),
        "NOV": Measure("%", 1.36),
        "DIC": Measure("%", 1.84)
    },
    "fixed_sys_monthly_cable_loss": {
        "GEN": Measure("%", 4.49),
        "FEB": Measure("%", 4.69),
        "MAR": Measure("%", 2.06),
        "APR": Measure("%", 4.44),
        "MAG": Measure("%", 3.19),
        "GIU": Measure("%", 3.79),
        "LUG": Measure("%", 2.27),
        "AGO": Measure("%", 3.98),
        "SET": Measure("%", 2.21),
        "OTT": Measure("%", 1.20),
        "NOV": Measure("%", 1.59),
        "DIC": Measure("%", 4.92)
    },
    "fixed_sys_monthly_inverter_loss": {
        "GEN": Measure("%", 4.84),
        "FEB": Measure("%", 1.08),
        "MAR": Measure("%", 2.63),
        "APR": Measure("%", 2.43),
        "MAG": Measure("%", 3.58),
        "GIU": Measure("%", 1.17),
        "LUG": Measure("%", 2.61),
        "AGO": Measure("%", 1.98),
        "SET": Measure("%", 4.52),
        "OTT": Measure("%", 3.79),
        "NOV": Measure("%", 1.23),
        "DIC": Measure("%", 1.43)
    },
    "fixed_sys_monthly_other_loss": {
        "GEN": Measure("%", 1.62),
        "FEB": Measure("%", 1.17),
        "MAR": Measure("%", 2.79),
        "APR": Measure("%", 1.38),
        "MAG": Measure("%", 1.44),
        "GIU": Measure("%", 4.61),
        "LUG": Measure("%", 2.09),
        "AGO": Measure("%", 3.37),
        "SET": Measure("%", 3.91),
        "OTT": Measure("%", 3.58),
        "NOV": Measure("%", 1.85),
        "DIC": Measure("%", 4.98)
      }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
