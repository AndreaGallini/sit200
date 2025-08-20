# P9 yearly energy production

import utils


class YearlyEnergyProduction:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.measurable_quantities = {
            "input": {
                "number_of_modules": {"value": 2500.0, "unit": ""},
                "annual_solar_radiation": {"value": 1700.0, "unit": "kWh/m2/anno"},
                "orientation_and_tilt_correction_factor": {"value": 1.1, "unit": ""},
                "module_area": {"value": 1.5, "unit": "m2"},
                "nominal_conversion_efficiency": {"value": 0.18, "unit": ""},
                "bos_conversion_efficiency": {"value": 0.95, "unit": ""},
                # "nominal_peak_power": {"value": 0.4, "unit": "kW"},
            },
            "output": {
                "yearly_energy_production": {"value": 8000.0, "unit": "kWh/anno"}
            }
        }

    def compute(self):
        number_of_modules = self.measurable_quantities['input']["number_of_modules"]["value"]
        annual_solar_radiation = self.measurable_quantities['input']['annual_solar_radiation']['value']
        orientation_and_tilt_correction_factor = (
            self.measurable_quantities['input']['orientation_and_tilt_correction_factor']['value']
        )
        module_area = self.measurable_quantities['input']['module_area']['value']
        nominal_conversion_efficiency = self.measurable_quantities['input']['nominal_conversion_efficiency']['value']
        bos_conversion_efficiency = self.measurable_quantities['input']['bos_conversion_efficiency']['value']
        # nominal_peak_power = self.measurable_quantities['input']['nominal_peak_power']['value']
        yearly_energy_production = (
                number_of_modules
                * annual_solar_radiation
                * orientation_and_tilt_correction_factor
                * module_area
                * nominal_conversion_efficiency
                * bos_conversion_efficiency
        )
        self.measurable_quantities['output']['yearly_energy_production']['value'] = tools.proper_round(
            yearly_energy_production
        )

    def validate(self):
        data_schema = {
            "number_of_modules": float,
            "annual_solar_radiation": float,
            "orientation_and_tilt_correction_factor": float,
            "module_area": float,
            "nominal_conversion_efficiency": float,
            "bos_conversion_efficiency": float,
            "nominal_peak_power": float
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
    the_target = YearlyEnergyProduction()
    the_target.main()
