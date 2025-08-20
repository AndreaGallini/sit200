# Black Modello B5 INGRESSI - Compatibilità ingressi
# in: parallel_strings_number, inverter_mppt_number
# out: inverter_mppt_parallel_string_compatibility

from concept import Measure, MeasureDerivation
import utils


class InverterMPPTParallelStringsCompatibility(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                'parallel_strings_number': the_input_data['parallel_strings_number'],
                'inverter_mppt_number': the_input_data['inverter_mppt_number'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'inverter_mppt_parallel_string_compatibility': Measure("bool", False)
        }

    def validate(self):
        for x in [ 'parallel_strings_number', 'inverter_mppt_number' ]:
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
        self.output['inverter_mppt_parallel_string_compatibility'] = Measure(
            "bool",
            self.input['parallel_strings_number'].value <= self.input['inverter_mppt_number'].value
        )


if __name__ == '__main__':
    the_target = InverterMPPTParallelStringsCompatibility(
        {
            'parallel_strings_number': Measure("", 10),
            'inverter_mppt_number': Measure("", 20),
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
