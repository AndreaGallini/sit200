# P6 actual grid-feed power

import utils


class ActualGridFeedPower:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "transformer_efficiency": {"value": 99.0, "unit": "%"},
                "cable_efficiency": {"value": 99.5, "unit": "%"},
                "inverter_output_power": {"value": 500000, "unit": "W"},
                "number_of_inverters": {"value": 11, "unit": ""},
                # "maximum_allowable_grid_feed_power": {"value": 30.5, "unit": "W"},
            },
            "output": {
                "actual_grid_feed_power": {"value": 5.0, "unit": "MW"}
            }
        }

    def compute(self):
        transformer_efficiency = self.measurable_quantities["input"]["transformer_efficiency"]["value"]
        cable_efficiency = self.measurable_quantities["input"]["cable_efficiency"]["value"]
        inverter_output_power = self.measurable_quantities["input"]["inverter_output_power"]["value"]
        number_of_inverters = self.measurable_quantities["input"]["number_of_inverters"]["value"]
        actual_grid_feed_power = (
                inverter_output_power
                * number_of_inverters
                * transformer_efficiency
                * cable_efficiency
                / 10000000000
        )
        self.measurable_quantities["output"]["actual_grid_feed_power"]["value"] = tools.proper_round(actual_grid_feed_power)

    def validate(self):
        data_schema = {
            "transformer_efficiency": float,
            "cable_efficiency": float,
            "inverter_output_power": float,
            "number_of_inverters": float
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
    the_target = ActualGridFeedPower()
    the_target.main()
