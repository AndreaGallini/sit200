# U1 Number of rooftop modules

import utils


class NumberOfRooftopModules:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "rooftop_system_power": {"value": 5, "unit": "kW"},
                "module_power": {"value": 400, "unit": "W"}
            },
            "output": {
                "number_of_rooftop_modules": {"value": 13, "unit": ""}
            }
        }

    def compute(self):
        rooftop_system_power = self.measurable_quantities['input']['rooftop_system_power']['value']
        module_power = self.measurable_quantities['input']['module_power']['value']
        number_of_rooftop_modules = tools.proper_round(rooftop_system_power * 1000 / module_power)
        self.measurable_quantities['output']['number_of_rooftop_modules']['value'] = number_of_rooftop_modules

    def validate(self):
        data_schema = {
                "rooftop_system_power": {"value": int, "unit": "kW"},
                "module_power": {"value": int, "unit": "W"}
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
            print(self.measurable_quantities['input'])
            for io in ['input', 'output']:
                for measurable_quantity, measurement in self.measurable_quantities[io].items():
                    value = measurement['value']
                    unit = measurement['unit']
                    label = measurable_quantity.replace('_', ' ')
                    print(f'{label}: {value} {unit}')


if __name__ == '__main__':
    the_target = NumberOfRooftopModules()
    the_target.main()
