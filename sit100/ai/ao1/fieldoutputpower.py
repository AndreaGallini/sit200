# P4 field output power

import utils


class FieldOutputPower:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "number_of_parallel_modules": {"value": 15.0, "unit": ""},
                "string_length": {"value": 12.0, "unit": ""},
                "yield_per_mppt": {"value": 98.5, "unit": "%"},
                "dc_cable_loss": {"value": 1.5, "unit": "%"},
                "mismatch_loss": {"value": 2.0, "unit": "%"},
                "effective_module_power_output": {"value": 320.0, "unit": "W"}
            },
            "output": {
                "field_output_power": {"value": 55.0, "unit": "kW"}
            }
        }

    def compute(self):
        number_of_parallel_modules = self.measurable_quantities["input"]["number_of_parallel_modules"]["value"]
        string_length = self.measurable_quantities["input"]["string_length"]["value"]
        yield_per_mppt = self.measurable_quantities["input"]["yield_per_mppt"]["value"]
        dc_cable_loss = self.measurable_quantities["input"]["dc_cable_loss"]["value"]
        mismatch_loss = self.measurable_quantities["input"]["mismatch_loss"]["value"]
        effective_module_power_output = self.measurable_quantities["input"]["effective_module_power_output"]["value"]
        field_output_power = (
                number_of_parallel_modules
                * string_length
                * yield_per_mppt / 100
                * (1 - dc_cable_loss / 100)
                * (1 - mismatch_loss / 100)
                * effective_module_power_output
                / 1000
        )
        self.measurable_quantities["output"]["field_output_power"]["value"] = tools.proper_round(field_output_power)

    def validate(self):
        data_schema = {
            "number_of_parallel_modules": float,
            "string_length": float,
            "yield_per_mppt": float,
            "dc_cable_loss": float,
            "mismatch_loss": float,
            "effective_module_power_output": float
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
    the_target = FieldOutputPower()
    the_target.main()
