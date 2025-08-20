# U3 rooftop yearly energy yield

import utils


class RooftopYearlyEnergyYield:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "rooftop_nameplate_power": {"value": 5, "unit": "kW"},
                "peak_sun_hours": {"value": 4, "unit": ""},
                "efficiency": {"value": 0.75, "unit": ""},
            },
            "output": {
                "rooftop_yearly_energy_yield": {"value": 5475.0, "unit": "kW"}
            }
        }

    def compute(self):
        rooftop_nameplate_power = self.measurable_quantities['input']['rooftop_nameplate_power']['value']
        peak_sun_hours = self.measurable_quantities['input']['peak_sun_hours']['value']
        efficiency = self.measurable_quantities['input']['efficiency']['value']
        rooftop_yearly_energy_yield = rooftop_nameplate_power * peak_sun_hours * efficiency * 365
        self.measurable_quantities['output']['rooftop_yearly_energy_yield']['value'] = rooftop_yearly_energy_yield

    def validate(self):
        data_schema = {
                "rooftop_nameplate_power": {"value": float, "unit": "kW"},
                "peak_sun_hours": {"value": int, "unit": ""},
                "efficiency": {"value": float, "unit": ""},
        }
        return tools.validate_input(self.measurable_quantities['input'], data_schema)

    def main(self, the_input_data=None, the_input_csv=None, the_output_csv=None):
        if the_input_data:
            self.input_data = the_input_data
            if self.validate():
                self.compute()
                return self.measurable_quantities['output']
            else:
                print('Input data not valid')
                return None
        elif the_input_csv and the_input_csv:
            self.measurable_quantities['input'] = tools.read_measurements(the_input_csv)
            if self.validate():
                self.compute()
                tools.write_measurements(the_output_csv, [
                    self.measurable_quantities['output']
                ])
                return None
            else:
                print("input data not valid")
                return None
        else:
            self.compute()
            for io in ['input', 'output']:
                for measurable_quantity, measurement in self.measurable_quantities[io].items():
                    value = measurement['value']
                    unit = measurement['unit']
                    label = measurable_quantity.replace('_', ' ')
                    print(f'{label}: {value} {unit}')


if __name__ == '__main__':
    the_target = RooftopYearlyEnergyYield()
    the_target.main()
