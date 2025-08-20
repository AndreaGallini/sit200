# Black Modello B4 TENSIONE V - Compatibilità finestra MPPT per i sottocampi
# DRAFT
# in:
# module_mpp_voltage_at_standard_temp,
# min_operating_temp,
# max_operating_temp,
# subfield_modules_per_string
# out:
# module_mpp_voltage_min_operating_temp,
# module_mpp_voltage_max_operating_temp,
# min_temp_mpp_string_voltage_per_subfield,
# max_temp_mpp_string_voltage_per_subfield,
# min_temp_mpp_voltage_string_inverter_compatibility_per_subfield, 
# max_temp_mpp_voltage_string_inverter_compatibility_per_subfield

from concept import Measure, MeasureDerivation
import utils


class SubFieldMPPTCompatibility(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                "module_mpp_voltage_at_standard_temp": the_input_data["module_mpp_voltage_at_standard_temp"],
                "min_operating_temp": the_input_data["min_operating_temp"],
                "max_operating_temp": the_input_data["max_operating_temp"],
                "temp_voc_conversion_percentage_coefficient":
                    the_input_data["temp_voc_conversion_percentage_coefficient"],
                "subfield_modules_per_string": the_input_data["subfield_modules_per_string"],
                'min_inverter_voltage': the_input_data["min_inverter_voltage"],
                'max_inverter_voltage': the_input_data["max_inverter_voltage"]
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "module_mpp_voltage_min_operating_temp": Measure("V", 0.0),
            "module_mpp_voltage_max_operating_temp": Measure("V", 0.0),
            "min_temp_mpp_string_voltage_per_subfield": Measure("V", 0.0),
            "max_temp_mpp_string_voltage_per_subfield": Measure("V", 0.0),
            "min_temp_mpp_voltage_string_inverter_compatibility_per_subfield": Measure("bool", 0.0),
            "max_temp_mpp_voltage_string_inverter_compatibility_per_subfield": Measure("bool", 0.0)
        }

    def validate(self):
        for x in [
            'module_mpp_voltage_at_standard_temp',
            'min_operating_temp',
            'max_operating_temp',
            'temp_voc_conversion_percentage_coefficient',
            'subfield_modules_per_string',
            'min_inverter_voltage',
            'max_inverter_voltage'
        ]:
            if x not in self.input:
                print(f"missing input value {x}")
                return False
        for x in [
            'module_mpp_voltage_at_standard_temp',
            'min_operating_temp',
            'max_operating_temp',
            'temp_voc_conversion_percentage_coefficient',
            'min_inverter_voltage',
            'max_inverter_voltage'
        ]:
            if not isinstance(self.input[x], Measure):
                print(f"input value {x} is not a measure")
                return False
        for x in [
            'module_mpp_voltage_at_standard_temp',
            'min_operating_temp',
            'max_operating_temp',
            'temp_voc_conversion_percentage_coefficient',
            'min_inverter_voltage',
            'max_inverter_voltage'
        ]:
            if not isinstance(self.input[x].value, (int, float)):
                print(f"input value {x} is not a number")
                return False
        if not isinstance(self.input["subfield_modules_per_string"], list):
            print(f"subfield_modules_per_string is not a list")
            return False
        for x in self.input["subfield_modules_per_string"]:
            if not isinstance(x, (int, float)):
                print(f"subfield_modules_per_string is not a measure or its value is not a number")
                return False
        return True

    def compute(self):
        module_mpp_voltage_at_standard_temp = self.input["module_mpp_voltage_at_standard_temp"].value
        min_operating_temp = self.input["min_operating_temp"].value
        max_operating_temp = self.input["max_operating_temp"].value
        subfield_modules_per_string = self.input["subfield_modules_per_string"]
        min_inverter_voltage = self.input["min_inverter_voltage"].value
        max_inverter_voltage = self.input["max_inverter_voltage"].value
        temp_voc_conversion_percentage_coefficient = (
            self.input["temp_voc_conversion_percentage_coefficient"].value
        )
        module_mpp_voltage_min_operating_temp = (
                module_mpp_voltage_at_standard_temp
                * (1 - (25-min_operating_temp) * temp_voc_conversion_percentage_coefficient / 100)
        )
        self.output['module_mpp_voltage_min_operating_temp'] = module_mpp_voltage_min_operating_temp
        module_mpp_voltage_max_operating_temp = (
            module_mpp_voltage_at_standard_temp
            * (1 + (max_operating_temp - 25) * temp_voc_conversion_percentage_coefficient / 100)
        )

        self.output['module_mpp_voltage_max_operating_temp'] = module_mpp_voltage_max_operating_temp
        for n in subfield_modules_per_string:
            min_temp_mpp_string_voltage_per_subfield = (
                Measure("V", tools.proper_round(module_mpp_voltage_min_operating_temp * n)))
            self.output['min_temp_mpp_string_voltage_per_subfield'] = min_temp_mpp_string_voltage_per_subfield
            max_temp_mpp_string_voltage_per_subfield = (
                Measure("V", tools.proper_round(module_mpp_voltage_max_operating_temp * n)))
            self.output['max_temp_mpp_string_voltage_per_subfield'] = max_temp_mpp_string_voltage_per_subfield
            min_temp_mpp_voltage_string_inverter_compatibility = (
                    min_temp_mpp_string_voltage_per_subfield.value <= max_inverter_voltage)
            self.output['min_temp_mpp_voltage_string_inverter_compatibility_per_subfield'] = (
                Measure("bool", min_temp_mpp_voltage_string_inverter_compatibility))
            max_temp_mpp_voltage_string_inverter_compatibility = (
                    max_temp_mpp_string_voltage_per_subfield.value >= min_inverter_voltage)
            self.output['max_temp_mpp_voltage_string_inverter_compatibility_per_subfield'] = (
                Measure("bool", max_temp_mpp_voltage_string_inverter_compatibility))


if __name__ == '__main__':
    the_target = SubFieldMPPTCompatibility(
        {
            "module_mpp_voltage_at_standard_temp": Measure("v", 300.0),
            "min_operating_temp": Measure("°C", 25.2),
            "max_operating_temp": Measure("°C", 30.2),
            "temp_voc_conversion_percentage_coefficient": Measure("%/°C", -35),
            "subfield_modules_per_string": [
                10, 12, 10
            ],
            'min_inverter_voltage': Measure("V", 250.0),
            'max_inverter_voltage': Measure("V", 350.0),
        }
    )
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
