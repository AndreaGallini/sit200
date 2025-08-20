# arancione RID1 RIDUZIONE DEI GAS SERRA GHG

from .concept import Measure, MeasureDerivation, months
from .utils import log
from .data.parameter_values import SYSTEM_LIFETIME, EFN2O, EFCO2, EFCH4, CH4_CO2, N2O_CO2


class GreenHouseGasesReduction(MeasureDerivation):
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
            "co2_reduction": Measure("kg CO2/anno", 0.0),
            "ch4_reduction": Measure("kg CH4/anno", 0.0),
            "n2o_reduction": Measure("kg N2O/anno", 0.0),
            "ch4_co2_eq_reduction": Measure("kg CO2/anno", 0.0),
            "n2o_co2_eq_reduction": Measure("kg CO2/anno", 0.0),
            "ghg_co2_eq_reduction_annual": Measure("kg CO2/anno", 0.0),
            "ghg_co2_eq_reduction_total": Measure("kg CO2/anno", 0.0),
            "ghg_co2_eq_reduction_total_tons": Measure("t CO2/anno", 0.0)
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
        # Passo 1: Calcolo Emissioni Evitate annue per Gas
        annual_energy_production = self.input['annual_energy_production'].value
        co2_reduction = annual_energy_production * EFCO2.value
        ch4_reduction = annual_energy_production * EFCH4.value
        n2o_reduction = annual_energy_production * EFN2O.value
        # Passo 2 conversione CH4 e N2O in CO2eq:
        ch4_co2_eq_reduction = ch4_reduction * CH4_CO2.value
        n2o_co2_eq_reduction = n2o_reduction * N2O_CO2.value
        # Passo 3 Calcolo Totale GHG Evitati Annui
        ghg_co2_eq_reduction_annual = co2_reduction + ch4_co2_eq_reduction + n2o_co2_eq_reduction
        # Passo 4 Calcolo GHG Totale in 20 Anni
        ghg_co2_eq_reduction_total = ghg_co2_eq_reduction_annual * SYSTEM_LIFETIME.value
        # Passo 5 Convertito in tonnellate:
        ghg_co2_eq_reduction_total_tons = ghg_co2_eq_reduction_total / 1000.0
        # output
        self.output['co2_reduction'] = Measure("kg CO2/anno", round(co2_reduction, 2))
        self.output['ch4_reduction'] = Measure("kg CH4/anno", round(ch4_reduction, 2))
        self.output['n2o_reduction'] = Measure("kg N2O/anno", round(n2o_reduction, 2))
        self.output['ch4_co2_eq_reduction'] = Measure("kg CO2/anno", round(ch4_co2_eq_reduction, 2))
        self.output['n2o_co2_eq_reduction'] = Measure("kg CO2/anno", round(n2o_co2_eq_reduction, 2))
        self.output['ghg_co2_eq_reduction_annual'] = Measure("kg CO2/anno", round(ghg_co2_eq_reduction_annual, 2))
        self.output['ghg_co2_eq_reduction_total'] = Measure("kg CO2/anno", round(ghg_co2_eq_reduction_total, 2))
        self.output['ghg_co2_eq_reduction_total_tons'] = Measure("t CO2/anno", round(ghg_co2_eq_reduction_total_tons, 2))


if __name__ == '__main__':
    the_target = GreenHouseGasesReduction({"annual_energy_production": Measure("kWh", 15000.0)})
    if the_target.validate():
        the_target.main()
        print(the_target.get_output(True))
    else:
        print("input not valid, error")
        print(the_target.dump())

