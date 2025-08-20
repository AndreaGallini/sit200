# P2 module MPP power

import utils


class ModuleMPPPower:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "irradiance": {"value": 1375.0, "unit": "W/m2"},
                "nominal_module_power": {"value": 400.0, "unit": "W"},
                "module_temperature": {"value": 65.0, "unit": "°C"},
                "temperature_coefficient": {"value": 0.0040, "unit": "1/°C"}  # attention to sign!
            },
            "output": {
                "module_mpp_power": {"value": 462.0, "unit": "W"}
            }
        }

    def compute(self):
        irradiance = self.measurable_quantities["input"]["irradiance"]["value"]
        nominal_module_power = self.measurable_quantities["input"]["nominal_module_power"]["value"]
        module_temperature = self.measurable_quantities["input"]["module_temperature"]["value"]
        temperature_coefficient = self.measurable_quantities["input"]["temperature_coefficient"]["value"]
        module_mpp_power = (
                nominal_module_power
                * (1 - temperature_coefficient * (module_temperature - 25))
                * irradiance
                / 1000
        )
        self.measurable_quantities['output']['module_mpp_power'] = {"value": module_mpp_power, "unit": "°C"}

    def validate(self):
        data_schema = {
            "irradiance": float,
            "nominal_module_power": float,
            "module_temperature": float,
            "temperature_coefficient": float
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
    the_target = ModuleMPPPower()
    the_target.main()
