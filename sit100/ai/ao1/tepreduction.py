# arancione RID1 RIDUZIONE DEI GAS SERRA GHG

from .concept import Measure, MeasureDerivation, months
from .utils import log
from .data.parameter_values import SYSTEM_LIFETIME, CTEP


class TEPReduction(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = { # from arancione EE10
                'annual_energy_production': the_input_data['annual_energy_production']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "tep_reduction": Measure("TEP", 0.0),
            "tep_reduction_comment": ""
        }

    def validate(self):
        if "annual_energy_production" not in self.input:
            log("ERROR", f"{__class__.__name__} missing input value")
            return False
        annual_energy_production = self.input['annual_energy_production']
        if not isinstance(annual_energy_production, Measure):
            log("ERROR", f"{__class__.__name__} input value is not a Measure")
            return False
        annual_energy_production = annual_energy_production.value
        if not isinstance(annual_energy_production, (float, int)):
            log("ERROR", f"{__class__.__name__} input value is not a number")
            return False
        return True

    def compute(self):
        annual_energy_production = self.input['annual_energy_production'].value
        tep_reduction = annual_energy_production * SYSTEM_LIFETIME.value / CTEP.value
        self.output['tep_reduction'] = Measure("TEP", round(tep_reduction, 2))
        self.output['tep_reduction_comment'] = f"{tep_reduction:.2f} TEP evitati in {SYSTEM_LIFETIME.value:.0f} anni di esercizio"


if __name__ == '__main__':
    the_target = TEPReduction({"annual_energy_production": Measure("kWh", 15000.0)})
    if the_target.validate():
        the_target.main()
        print(the_target.get_output(True))
    else:
        print("input not valid, error")
        print(the_target.dump())

