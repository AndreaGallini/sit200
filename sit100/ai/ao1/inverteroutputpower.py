# P5 inverter output power

import utils


class InverterOutputPower:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "max_inverter_output_power": {"value": 6000.0, "unit": "W"},
                "field_output_power": {"value": 5500.0, "unit": "W"},
                "inverter_yield": {"value": 98.0, "unit": "%"},
                "inverter_self_power_consumption": {"value": 30.5, "unit": "W"}
            },
            "output": {
                "inverter_output_power": {"value": 5470.0, "unit": "W"}
            }
        }

    def compute(self):
        max_inverter_output_power = self.measurable_quantities["input"]["max_inverter_output_power"]["value"]
        field_output_power = self.measurable_quantities["input"]["field_output_power"]["value"]
        inverter_yield = self.measurable_quantities["input"]["inverter_yield"]["value"]
        inverter_self_power_consumption = self.measurable_quantities["input"]["inverter_self_power_consumption"]["value"]
        if field_output_power <= inverter_self_power_consumption:
            self.measurable_quantities['output']['inverter_output_power']['value'] = 0
        else:
            inverter_output_power = min(field_output_power, max_inverter_output_power) * inverter_yield / 100
            inverter_output_power = tools.proper_round(inverter_output_power)
            self.measurable_quantities["output"]["inverter_output_power"]["value"] = inverter_output_power

    def validate(self):
        data_schema = {
            "max_inverter_output_power": float,
            "field_output_power": float,
            "inverter_yield": float,
            "inverter_self_power_consumption": float
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
    the_target = InverterOutputPower()
    the_target.main()
