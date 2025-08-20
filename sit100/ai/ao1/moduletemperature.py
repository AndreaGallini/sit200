# P1 module temperature

import utils


class ModuleTemperature:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "annual_irradiation": {"value": 5.5, "unit": "kW"},
                "peak_sun_hours": {"value": 4.0, "unit": ""},
                "ambient_temperature": {"value": 28.0, "unit": "°C"},
                "nominal_operating_cell_temperature": {"value": 45.0, "unit": "°C"}
            },
            "output": {
                "module_temperature": {"value": 65.0, "unit": "°C"}
            }
        }

    def compute(self):
        annual_irradiation = self.measurable_quantities["input"]["annual_irradiation"]["value"]
        peak_sun_hours = self.measurable_quantities["input"]["peak_sun_hours"]["value"]
        ambient_temperature = self.measurable_quantities["input"]["ambient_temperature"]["value"]
        nominal_operating_cell_temperature = self.measurable_quantities["input"]["nominal_operating_cell_temperature"]["value"]
        annual_irradiation = annual_irradiation * 1000 / peak_sun_hours
        module_temperature = ambient_temperature + annual_irradiation * (nominal_operating_cell_temperature-20) / 800
        module_temperature = tools.proper_round(module_temperature, 1)
        self.measurable_quantities["output"]["module_temperature"] = {"value": module_temperature, "unit": "°C"}

    def validate(self):
        data_schema = {
            "annual_irradiation": float,
            "peak_sun_hours": float,
            "ambient_temperature": float,
            "nominal_operating_cell_temperature": float
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
    the_target = ModuleTemperature()
    the_target.main()
