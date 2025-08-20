# arancione ITE 13 riassunto efficienze di sistema per mese escluso ombreggiamento
from .concept import Measure, MeasureDerivation, months
from .utils import log


def key_loss2efficiency(key_loss):
    key_efficiency = key_loss.rsplit("_", 1)[0] + "_efficiency"
    return key_efficiency

class MonthlySystemEfficiencySummary(MeasureDerivation):

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
            missing_keys = [key for key in [
                'fixed_sys_monthly_temp_loss',
                'fixed_sys_monthly_reflection_loss',
                'fixed_sys_monthly_soiling_loss',
                'fixed_sys_monthly_low_irradiance_loss',
                'fixed_sys_monthly_mismatching_loss',
                'fixed_sys_monthly_cable_loss',
                'fixed_sys_monthly_inverter_loss',
                'fixed_sys_monthly_other_loss'
            ] if key not in the_input_data]
            print(f"Missing keys: {missing_keys}")
            quit()
        self.output = {'monthly_system_efficiency_summary':
            {key_loss2efficiency(key): {month: Measure('%', 0.0) for month in months} for key in self.input}}

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
        return True

    def compute(self):
        for key, monthly_values in self.input.items():
            for month, loss in monthly_values.items():
                efficiency_value = 100.0 - loss.value
                efficiency = Measure("%", efficiency_value)
                key_efficiency = key_loss2efficiency(key)
                if key_efficiency not in self.output['monthly_system_efficiency_summary']:
                    self.output['monthly_system_efficiency_summary'][key_efficiency] = {month: efficiency}
                else:
                    self.output['monthly_system_efficiency_summary'][key_efficiency][month] = efficiency


if __name__ == "__main__":
    the_target = MonthlySystemEfficiencySummary({
                "fixed_sys_monthly_temp_loss": {
                    "GEN": Measure("%", -1.91),
                    "FEB": Measure("%", -0.22),
                    "MAR": Measure("%", 4.05),
                    "APR": Measure("%", 9.23),
                    "MAG": Measure("%", 13.84),
                    "GIU": Measure("%", 18.34),
                    "LUG": Measure("%", 20.93),
                    "AGO": Measure("%", 20.70),
                    "SET": Measure("%", 17.33),
                    "OTT": Measure("%", 11.14),
                    "NOV": Measure("%", 5.06),
                    "DIC": Measure("%", 0.00),
                },
                "fixed_sys_monthly_reflection_loss": {
                    "GEN": Measure("%", 3.00),
                    "FEB": Measure("%", 3.00),
                    "MAR": Measure("%", 3.00),
                    "APR": Measure("%", 3.00),
                    "MAG": Measure("%", 3.00),
                    "GIU": Measure("%", 4.00),
                    "LUG": Measure("%", 3.00),
                    "AGO": Measure("%", 3.00),
                    "SET": Measure("%", 4.00),
                    "OTT": Measure("%", 3.00),
                    "NOV": Measure("%", 3.00),
                    "DIC": Measure("%", 4.00),
                },
                "fixed_sys_monthly_soiling_loss": {
                    "GEN": Measure("%", 1.00),
                    "FEB": Measure("%", 1.00),
                    "MAR": Measure("%", 4.00),
                    "APR": Measure("%", 1.00),
                    "MAG": Measure("%", 3.00),
                    "GIU": Measure("%", 1.00),
                    "LUG": Measure("%", 1.00),
                    "AGO": Measure("%", 2.00),
                    "SET": Measure("%", 1.00),
                    "OTT": Measure("%", 1.00),
                    "NOV": Measure("%", 1.00),
                    "DIC": Measure("%", 1.00),
                },
                "fixed_sys_monthly_low_irradiance_loss": {
                    "GEN": Measure("%", 2.42),
                    "FEB": Measure("%", 2.42),
                    "MAR": Measure("%", 2.42),
                    "APR": Measure("%", 2.42),
                    "MAG": Measure("%", 4.42),
                    "GIU": Measure("%", 2.42),
                    "LUG": Measure("%", 2.42),
                    "AGO": Measure("%", 2.42),
                    "SET": Measure("%", 3.42),
                    "OTT": Measure("%", 2.42),
                    "NOV": Measure("%", 2.42),
                    "DIC": Measure("%", 2.42),
                },
                "fixed_sys_monthly_mismatching_loss": {
                    "GEN": Measure("%", 0.00),
                    "FEB": Measure("%", 0.00),
                    "MAR": Measure("%", 0.00),
                    "APR": Measure("%", 0.00),
                    "MAG": Measure("%", 0.00),
                    "GIU": Measure("%", 0.00),
                    "LUG": Measure("%", 0.00),
                    "AGO": Measure("%", 0.00),
                    "SET": Measure("%", 0.00),
                    "OTT": Measure("%", 0.00),
                    "NOV": Measure("%", 0.00),
                    "DIC": Measure("%", 0.00),
                },
                "fixed_sys_monthly_cable_loss": {
                    "GEN": Measure("%", -0.67),
                    "FEB": Measure("%", -0.67),
                    "MAR": Measure("%", -0.67),
                    "APR": Measure("%", -0.67),
                    "MAG": Measure("%", -0.67),
                    "GIU": Measure("%", -0.67),
                    "LUG": Measure("%", -0.67),
                    "AGO": Measure("%", -0.67),
                    "SET": Measure("%", -0.67),
                    "OTT": Measure("%", -0.67),
                    "NOV": Measure("%", -0.67),
                    "DIC": Measure("%", -0.67),
                },
                "fixed_sys_monthly_inverter_loss": {
                    "GEN": Measure("%", -2.00),
                    "FEB": Measure("%", -2.00),
                    "MAR": Measure("%", -2.00),
                    "APR": Measure("%", -2.00),
                    "MAG": Measure("%", -2.00),
                    "GIU": Measure("%", -2.00),
                    "LUG": Measure("%", -2.00),
                    "AGO": Measure("%", -2.00),
                    "SET": Measure("%", -2.00),
                    "OTT": Measure("%", -2.00),
                    "NOV": Measure("%", -2.00),
                    "DIC": Measure("%", -2.00),
                },
                "fixed_sys_monthly_other_loss": {
                    "GEN": Measure("%", 0.00),
                    "FEB": Measure("%", 0.00),
                    "MAR": Measure("%", 0.00),
                    "APR": Measure("%", 0.00),
                    "MAG": Measure("%", 0.00),
                    "GIU": Measure("%", 0.00),
                    "LUG": Measure("%", 0.00),
                    "AGO": Measure("%", 0.00),
                    "SET": Measure("%", 0.00),
                    "OTT": Measure("%", 0.00),
                    "NOV": Measure("%", 0.00),
                    "DIC": Measure("%", 0.00),
                },
            }
        )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
