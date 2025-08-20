# P7 actual grid feed energy

import utils


class ActualGridFeedEnergy:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "grid_feed_efficiency": {"value": 99.5, "unit": "%"},
                "solar_peek_hours": {"value": 2000.0, "unit": ""},
                "actual_grid_feed_power": {"value": 5.3, "unit": "MW"},
            },
            "output": {
                "total_energy_fed_into_grid": {"value": 5.0, "unit": "MWh"}
            }
        }

    def compute(self):
        grid_feed_efficiency = self.measurable_quantities["input"]["grid_feed_efficiency"]["value"]
        solar_peek_hours = self.measurable_quantities["input"]["solar_peek_hours"]["value"]
        actual_grid_feed_power = self.measurable_quantities["input"]["actual_grid_feed_power"]["value"]
        total_energy_fed_into_grid = grid_feed_efficiency * solar_peek_hours * actual_grid_feed_power / 100
        self.measurable_quantities['output']['total_energy_fed_into_grid']['value'] = total_energy_fed_into_grid

    def validate(self):
        data_schema = {
            "grid_feed_efficiency": float,
            "solar_peek_hours": float,
            "actual_grid_feed_power": float
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
    the_target = ActualGridFeedEnergy()
    the_target.main()
