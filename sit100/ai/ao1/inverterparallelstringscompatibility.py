# Black Modello B6 CORRENTE I - Compatibilità corrente I
# in: strings_number, module_current
# out: max_generator_current, inverter_parallel_string_compatibility

from concept import Measure, MeasureDerivation
import utils


class InverterParallelStringsCompatibility(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                'strings_number': the_input_data['strings_number'],
                'module_current': the_input_data['module_current'],
                'max_inverter_input_current': the_input_data['max_inverter_input_current']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'max_generator_current': Measure("A", 0.0),
            'inverter_parallel_string_compatibility': Measure("bool", False)
        }

    def validate(self):
        for x in ['strings_number', 'module_current', 'max_inverter_input_current']:
            if x not in self.input:
                print(f"missing input value {x}")
                return False
            if not isinstance(self.input[x], Measure):
                print(f"input value {x} is not a measure")
                return False
            if not isinstance(self.input[x].value, (int, float)):
                print(f"input value {x} is not a number")
                return False
        return True

    def compute(self):
        max_generator_current = self.input['module_current'].value * self.input['strings_number'].value
        self.output['max_generator_current'] = Measure("A", max_generator_current)
        self.output['inverter_parallel_string_compatibility'] = Measure(
            "bool",
            max_generator_current <= self.input['max_inverter_input_current'].value)


if __name__ == '__main__':
    the_target = InverterParallelStringsCompatibility(
        {
            'strings_number': Measure("", 20),
            'module_current': Measure("A", 16.66),
            'max_inverter_input_current': Measure("A", 360.0)
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
