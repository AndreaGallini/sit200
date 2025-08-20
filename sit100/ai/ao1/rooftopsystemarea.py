# U2 rooftop system area

import utils


class RooftopSystemArea:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "number_of_rooftop_modules": {"value": 13, "unit": ""},
                "module_area": {"value": 1.7, "unit": "m2"}
            },
            "output": {
                "rooftop_system_area": {"value": 22.1, "unit": "m2"}
            }
        }

    def compute(self):
        number_of_rooftop_modules = self.measurable_quantities['input']['number_of_rooftop_modules']['value']
        module_area = self.measurable_quantities['input']['module_area']['value']
        rooftop_system_area = tools.proper_round(number_of_rooftop_modules * module_area, 1)
        self.measurable_quantities['output']['rooftop_system_area']['value'] = rooftop_system_area

    def validate(self):
        data_schema = {
                "number_of_rooftop_modules": {"value": int, "unit": ""},
                "module_area": {"value": float, "unit": "m2"}
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
    the_target = RooftopSystemArea()
    the_target.main()
