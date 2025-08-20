# Black Modello B7 compatibilità tensione a vuoto voc
# in: temp_voc_conversion_coeff_pct, module_voc, min_operating_temp, string_modules_per_subfield
# out: min_temp_voc_voltage, min_temp_string_voc_per_subfield, max_generator_voc, generator_inverter_voc_compatibility

from concept import Measure, MeasureDerivation
import utils


class GeneratorInverterVocCompatibility(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                'temp_voc_conversion_coeff_pct': the_input_data['temp_voc_conversion_coeff_pct'],
                'module_voc': the_input_data['module_voc'],
                'min_operating_temp': the_input_data['min_operating_temp'],
                'string_modules_per_subfield': the_input_data['string_modules_per_subfield'],
                'max_inverter_input_voltage': the_input_data['max_inverter_input_voltage']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'min_temp_voc_voltage': Measure("V", 0.0),
            'min_temp_string_voc_per_subfield': [],
            'max_generator_voc': Measure("V", 0.0),
            'generator_inverter_voc_compatibility': Measure("bool", False),
        }

    def validate(self):
        for x in ['temp_voc_conversion_coeff_pct', 'module_voc', 'min_operating_temp', 'string_modules_per_subfield',
                  'max_inverter_input_voltage']:
            if x not in self.input:
                print(f"missing input value {x}")
                return False
        for x in ['temp_voc_conversion_coeff_pct', 'module_voc', 'min_operating_temp']:
            if not isinstance(self.input[x], Measure):
                print(f"input value {x} is not a measure")
                return False
            if not isinstance(self.input[x].value, (int, float)):
                print(f"input value {x} is not a number")
                return False
        if not isinstance(self.input['string_modules_per_subfield'], list):
            print(f"output value {x} is not a list")
            return False
        for n in self.input['string_modules_per_subfield']:
            if not isinstance(n, (int, float)):
                print(f"input value {n} is not a number")
                return False
        return True

    def compute(self):
        temp_voc_conversion_coeff_pct = self.input['temp_voc_conversion_coeff_pct'].value
        module_voc = self.input['module_voc'].value
        min_operating_temp = self.input['min_operating_temp'].value
        string_modules_per_subfield = self.input['string_modules_per_subfield']
        max_inverter_input_voltage = self.input['max_inverter_input_voltage'].value
        min_temp_voc_voltage = module_voc * (1-(25-min_operating_temp)*temp_voc_conversion_coeff_pct/100)
        self.output['min_temp_voc_voltage'].value = min_temp_voc_voltage
        min_temp_string_voc_per_subfield = []
        for subfield in string_modules_per_subfield:
            min_temp_string_voc_per_subfield.append(
                Measure("V", tools.proper_round(min_temp_voc_voltage * subfield)))
        self.output['min_temp_string_voc_per_subfield'] = min_temp_string_voc_per_subfield
        max_generator_voc = max([x.value for x in min_temp_string_voc_per_subfield ])
        self.output['max_generator_voc'] = max_generator_voc
        generator_inverter_voc_compatibility = max_generator_voc <= max_inverter_input_voltage
        self.output['generator_inverter_voc_compatibility'] = Measure("bool", generator_inverter_voc_compatibility)


if __name__ == '__main__':
    the_target = GeneratorInverterVocCompatibility(
        {
            'temp_voc_conversion_coeff_pct': Measure("%/°C", -35.0),
            'module_voc': Measure("V", 350.0),
            'min_operating_temp': Measure("°C", 22.3),
            'string_modules_per_subfield': [12,22,33],
            'max_inverter_input_voltage': Measure("V", 37200.0)
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
