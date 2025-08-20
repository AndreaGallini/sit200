# P3 effective module power output

import utils


class EffectiveModulePowerOutput:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "soiling_power_loss_percent": {"value": 5, "unit": "%"},
                "shading_power_loss_percent": {"value": 3, "unit": "%"},
                "module_output_power": {"value": 320.0, "unit": "W"}
            },
            "output": {
                "effective_module_power_output": {"value": 304.0, "unit": "W"},
                "power_loss_per_module": {"value": 96.0, "unit": "W"},
            }
        }

    def compute(self):
        soiling_power_loss_percent = self.measurable_quantities["input"]["soiling_power_loss_percent"]['value']
        shading_power_loss_percent = self.measurable_quantities["input"]["shading_power_loss_percent"]['value']
        module_output_power = self.measurable_quantities["input"]["module_output_power"]['value']
        effective_module_power_output = (
            (1 - soiling_power_loss_percent / 100)
            * (1 - shading_power_loss_percent / 100)
            * module_output_power
        )
        power_loss_per_module = module_output_power - effective_module_power_output
        effective_module_power_output = tools.proper_round(effective_module_power_output)
        power_loss_per_module = tools.proper_round(power_loss_per_module)
        self.measurable_quantities['output']['effective_module_power_output'] = {"value": effective_module_power_output, "unit": "W"}
        self.measurable_quantities['output']['power_loss_per_module'] = {"value": power_loss_per_module, "unit": "W"}

    def validate(self):
        data_schema = {
            "soiling_power_loss_percent": float,
            "shading_power_loss_percent": float,
            "module_output_power": float
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
    the_target = EffectiveModulePowerOutput()
    the_target.main()
