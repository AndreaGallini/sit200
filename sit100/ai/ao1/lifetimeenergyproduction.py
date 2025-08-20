# P8 Lifetime Energy Production

import utils


class LifetimeEnergyProduction:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "yearly_energy_production": {"value": 10000.0, "unit": "MWh"},
                "lifetime": {"value": 25.0, "unit": ""},
                "degradation_factor": {"value": 80.0, "unit": "%"},
            },
            "output": {
                "lifetime_energy_production": {"value": 250000.0, "unit": "MWh"}
            }
        }

    def compute(self):
        yearly_energy_production = self.measurable_quantities['input']['yearly_energy_production']['value']
        lifetime = self.measurable_quantities['input']['lifetime']['value']
        degradation_factor = self.measurable_quantities['input']['degradation_factor']['value']
        lifetime_energy_production = yearly_energy_production * lifetime * degradation_factor / 100
        self.measurable_quantities['output']['lifetime_energy_production']['value'] = tools.proper_round(
            lifetime_energy_production
        )

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
    the_target = LifetimeEnergyProduction()
    the_target.main()
