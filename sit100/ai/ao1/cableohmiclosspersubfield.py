# Black Black CAVI 2 CORRENTE CONTINUA Perdita ohmica P% = V% per sottocampo [%]
# in: cable_capacity_per_subfield, mpp_module_stc_voltage, string_modules_number_per_subfield,
# max_cable_length_per_subfield, nominal_current_per_subfield
# out: cable_resistance_per_subfield, mpp_string_stc_voltage, cable_ohmic_loss_pct_per_subfield

from concept import Measure, MeasureDerivation
import utils


class CableOhmicLossPerSubfield(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                'mpp_module_stc_voltage': the_input_data['mpp_module_stc_voltage'],
                'cable_capacity_per_subfield': the_input_data['cable_capacity_per_subfield'],
                'string_modules_number_per_subfield': the_input_data['string_modules_number_per_subfield'],
                'max_cable_length_per_subfield': the_input_data['max_cable_length_per_subfield'],
                'nominal_current_per_subfield': the_input_data['nominal_current_per_subfield']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'cable_resistance_per_subfield': [],
            'mpp_string_stc_voltage_per_subfield': [],
            'cable_ohmic_loss_pct_per_subfield': [],
        }

    def validate(self):
        for x in ['mpp_module_stc_voltage', 'cable_capacity_per_subfield', 'string_modules_number_per_subfield',
                  'max_cable_length_per_subfield', 'nominal_current_per_subfield']:
            if x not in self.input:
                print(f"missing input value {x}")
                return False
        if not isinstance(self.input['mpp_module_stc_voltage'], Measure):
            print(f"input value {x} is not a measure")
            return False
        if not isinstance(self.input['mpp_module_stc_voltage'].value, (int, float)):
            print(f"input value {x} is not a number")
            return False
        for x in ['cable_capacity_per_subfield', 'string_modules_number_per_subfield',
                  'max_cable_length_per_subfield', 'nominal_current_per_subfield']:
            if not isinstance(self.input[x], list):
                print(f"input value {x} is not a list")
                return False
            for n in self.input[x]:
                if not isinstance(n, Measure):
                    print(f"input value {n} is not a measure")
                    return False
                elif x in ['cable_capacity_per_subfield', 'nominal_current_per_subfield']:
                    if n.unit != "A":
                        print(f"a measure of {x} is not in Ampere units")
                        return False
                elif x == 'string_modules_number_per_subfield':
                    if n.unit != "":
                        print(f"a measure of {x} is not a counting")
                        return False
                elif x == 'max_cable_length_per_subfield':
                    if n.unit != "m":
                        print(f"a measure of {x} is not in m")
                        return False
        return True

    def compute(self):
        mpp_module_stc_voltage = self.input['mpp_module_stc_voltage'].value
        cable_capacity_per_subfield = self.input['cable_capacity_per_subfield']
        string_modules_number_per_subfield = self.input['string_modules_number_per_subfield']
        max_cable_length_per_subfield = self.input['max_cable_length_per_subfield']
        nominal_current_per_subfield = self.input['nominal_current_per_subfield']
        cable_resistance_per_subfield = []
        for cable_capacity in cable_capacity_per_subfield:
            the_cable_capacity, the_cable_resistance = tools.cable_resistance_by_capacity(cable_capacity.value)
            cable_resistance_per_subfield.append(Measure("Ohm/km", the_cable_resistance))
        self.output['cable_resistance_per_subfield'] = cable_resistance_per_subfield
        mpp_string_stc_voltage_per_subfield = []
        for string_modules_number in string_modules_number_per_subfield:
            mpp_string_stc_voltage = mpp_module_stc_voltage * string_modules_number.value
            mpp_string_stc_voltage_per_subfield.append(Measure("V", mpp_string_stc_voltage))
        self.output['mpp_string_stc_voltage_per_subfield'] = mpp_string_stc_voltage_per_subfield
        cable_ohmic_loss_pct_per_subfield = []
        for i, max_cable_length_measure in enumerate(max_cable_length_per_subfield):
            max_cable_length = max_cable_length_measure.value
            cable_resistance = cable_resistance_per_subfield[i].value
            nominal_current = nominal_current_per_subfield[i].value
            mpp_string_stc_voltage = mpp_string_stc_voltage_per_subfield[i].value
            cable_ohmic_loss_pct = (2 * cable_resistance * nominal_current * max_cable_length
                                    / mpp_string_stc_voltage / 1000)
            cable_ohmic_loss_pct_per_subfield.append(Measure("%", cable_ohmic_loss_pct))
        self.output['cable_ohmic_loss_pct_per_subfield'] = cable_ohmic_loss_pct_per_subfield


if __name__ == '__main__':
    the_target = CableOhmicLossPerSubfield(
        {
            'mpp_module_stc_voltage': Measure("V", 430.0),
            'cable_capacity_per_subfield': [
                Measure("A", 20.3),
                Measure("A", 33.3),
                Measure("A", 60.8)
            ],
            'string_modules_number_per_subfield': [
                Measure("", 30),
                Measure("", 20),
                Measure("", 44),
            ],
            'max_cable_length_per_subfield': [
                Measure("m", 125),
                Measure("m", 62),
                Measure("m", 74)
            ],
            'nominal_current_per_subfield': [
                Measure("A", 22.5),
                Measure("A", 31.3),
                Measure("A", 15.3)
            ]
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
