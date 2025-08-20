# Black CAVI 1 CORRENTE CONTINUA Sezione cavo per sottocampo, definita dalla portata
# in: module_current, string_number_per_subfield
# out: nominal_current_per_subfield, min_switch_current_threshold_per_subfield

from concept import Measure, MeasureDerivation
import utils


class CableSectionPerSubfield(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                'module_current': the_input_data['module_current'],
                'string_number_per_subfield': the_input_data['string_number_per_subfield']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'nominal_current_per_subfield': [],
            'min_switch_current_threshold_per_subfield': [],
            'cable_capacity_per_subfield': [],
            'cable_section_per_subfield': []
        }

    def validate(self):
        for x in ['module_current', 'string_number_per_subfield']:
            if x not in self.input:
                print(f"missing input value {x}")
                return False
        if not isinstance(self.input['module_current'], Measure):
            print(f"input value {x} is not a measure")
            return False
        if not isinstance(self.input['module_current'].value, (int, float)):
            print(f"input value {x} is not a number")
            return False
        if not isinstance(self.input['string_number_per_subfield'], list):
            print(f"output value {x} is not a list")
            return False
        for n in self.input['string_number_per_subfield']:
            if not isinstance(n, (int, float)):
                print(f"input value {n} is not a number")
                return False
        return True

    def compute(self):
        module_current = self.input['module_current'].value
        string_number_per_subfield = self.input['string_number_per_subfield']
        nominal_current_per_subfield = []
        min_switch_current_threshold_per_subfield = []
        cable_capacity_per_subfield = []
        cable_section_per_subfield = []
        for strings_number in string_number_per_subfield:
            nominal_current = strings_number * module_current
            min_switch_current_threshold = nominal_current * 1.1
            nominal_current_per_subfield.append(Measure("A", tools.proper_round(nominal_current)))
            min_switch_current_threshold_per_subfield.append(
                Measure("A", tools.proper_round(min_switch_current_threshold)))
            the_capacity, the_section = tools.cable_section_by_capacity(min_switch_current_threshold)
            cable_capacity_per_subfield.append(Measure("A", the_capacity))
            cable_section_per_subfield.append(Measure("mm", the_section))
        self.output['nominal_current_per_subfield'] = nominal_current_per_subfield
        self.output['min_switch_current_threshold_per_subfield'] = min_switch_current_threshold_per_subfield
        self.output['cable_capacity_per_subfield'] = cable_capacity_per_subfield
        self.output['cable_section_per_subfield'] = cable_section_per_subfield


if __name__ == '__main__':
    the_target = CableSectionPerSubfield(
        {
            'module_current': Measure("A", 1.3),
            'string_number_per_subfield': [22, 33, 44]
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
