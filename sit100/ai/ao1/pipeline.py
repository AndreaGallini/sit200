from datetime import datetime

from .databank import DataBank
from .concept import Measure

from .concept import Measure, dictMeasure2dict
from .databank import DataBank
from .utils import log

# SOLE10349
from .monthlyavgdailytemperature import MonthlyAvgDailyTemperature
from .annualavgtemperature import AnnualAvgTemperature
from .monthlyavghorizontalirradianceuni10349 import MonthlyAvgHorizontalIrradianceUni10349
from .monthlyavgdailyarrayirradianceuni10349 import MonthlyAvgDailyArrayIrradianceUni10349
from .monthlyplaneofarrayirradiance import MonthlyPlaneOfArrayIrradiance
from .annualsolarradiation import AnnualSolarRadiation
from .theoreticalannualyield import TheoreticalAnnualYield
from .monthlyavgdaylighthours import MonthlyAvgDaylightHours
from .annualavgdaylighthours import AnnualAvgDaylightHours
from .monthlyavgdailyarrayirradianceclassification import MonthlyAvgDailyArrayIrradianceClassification
from .monthlyavgdailyhorizontalsolarirradiancesummary import MonthlyAvgDailyHorizontalSolarIrradianceSummary

# LOSSES
from .fixedsysmonthlytemploss import FixedSysMonthlyTempLoss
from .fixedsysmonthlyempiricaltemploss import FixedSysMonthlyEmpiricalTempLoss
from .fixedsysmonthlyreflectionloss import FixedSysMonthlyReflectionLoss
from .fixedsysmonthlysoilingloss import FixedSysMonthlySoilingLoss
from .fixedsysmonthlylowirradianceloss import FixedSysMonthlyLowIrradianceLoss
from .fixedsysmonthlymismatchingloss import FixedSysMonthlyMismatchingLoss
from .fixedsysmonthlycableloss import FixedSysMonthlyCableLoss
from .fixedsysmonthlyinverterloss import FixedSysMonthlyInverterLoss
from .fixedsysmonthlyotherloss import FixedSysMonthlyOtherLoss
from .fixedsysmonthlyobstacleshading import FixedSysMonthlyObstacleShading
from .fixedsysmonthlyclinometricshading import FixedSysMonthlyClinometricShading
from .fixedsysmonthlyshadinglosspercentage import FixedSysMonthlyShadingLossPercentage
from .fixedsysmonthlyshadingloss import FixedSysMonthlyShadingLoss
from .fixedsysannualshadingloss import FixedSysAnnualShadingLoss
from .monthlysystemlossessummary import MonthlySystemLossesSummary
from .monthlysystemefficiencysummary import MonthlySystemEfficiencySummary

# ENERGY
from .monthlynetenergy import MonthlyNetEnergy
from .annualnetenergy import AnnualNetEnergy
from .monthlyefficiencypercentage import MonthlyEfficiencyPercentage
from .monthlyenergyyield import MonthlyEnergyYield
from .annualenergyyield import AnnualEnergyYield
from .systemefficiency import SystemEfficiency
from .dailyavgenergyyield import DailyAvgEnergyYield
from .dailyenergyyield import DailyEnergyYield
from .monthlyavgenergyproduction import MonthlyAvgEnergyProduction
from .annualenergyproduction import AnnualEnergyProduction
from .annuallosspercentage import AnnualLossPercentage
from .annuallosspercentageclassification import AnnualLossPercentageClassification
from .annualnetenergyclassification import AnnualNetEnergyClassification
from .systemefficiencyclassification import SystemEfficiencyClassification
from .tepreduction import TEPReduction
from .greenhousegasesreduction import GreenHouseGasesReduction

class Pipeline:
    def __init__(self, db: DataBank, expected_data: dict, name="The Pipeline") -> None:
        self.name = name
        self.expected_data = expected_data
        self.pipeline = []
        self.db = db
        self.prepare()

    def prepare(self) -> None:
        """
        from raw user data to Measures: data and measure units
        given parameter names must be as expected
        """
        for parameter, measure_unit in self.expected_data.items():
            user_data = self.db.get_output("UserData")
            if parameter in user_data:
                if isinstance(user_data[parameter], Measure):
                    #print("preparing", parameter, measure_unit)
                    continue
                if isinstance(measure_unit, dict):
                    for the_key, the_measure_prototype in self.expected_data[parameter].items():
                        if the_key not in user_data[parameter]:
                            log("ERROR", f"{the_key} not found in {parameter}")
                            quit()
                        if not isinstance(the_measure_prototype, Measure):
                            log("ERROR", f"{the_key} of  {parameter} is not a Measure")
                            quit()
                        user_data_value = user_data[parameter][the_key]
                        if isinstance(user_data_value, Measure):
                            continue
                        if not isinstance(user_data_value, (float, int)):
                            log("ERROR", f"{the_key} in {parameter} not of type {type(the_measure_prototype.value)}")
                            quit()
                        if isinstance(the_measure_prototype.value, (float, int)):
                            user_data[parameter][the_key] = Measure(the_measure_prototype.unit,
                                                                         float(user_data_value))
                        else:
                            parameter_type = the_measure_prototype
                            log("ERROR", f"{the_measure_prototype.value} of  {parameter} is not int nor float")
                            quit()
                elif isinstance(user_data[parameter], (float, int)):
                    user_data[parameter] = Measure(measure_unit, float(user_data[parameter]))
                else:
                    #print(user_data)
                    #print(user_data[parameter])
                    #print(type(user_data[parameter]))
                    parameter_type = type(user_data[parameter])
                    log("ERROR", f"user input {parameter} ({parameter_type}) is not a float or integer")
                    quit()
            else:
                log("ERROR", f"{parameter} is missing")
                quit()

    def compute(self, model):
        log("DEBUG", f"{self.name}: now computing model {model}")
        if model in self.db.input:
            in_data = self.db.get_input(model)
            # print(f"dati di input di {model}", in_data)
            try:
                model_class = globals()[model]
                try:
                    model_instance = model_class(in_data)
                    try:
                        log("DEBUG", f"{self.name} - {model}: validating...")
                        model_instance.validate()
                        log("DEBUG", f"{self.name} - {model}: computing...")
                        model_instance.compute()
                        # log: DEBUG: input ed output del modello
                        data = model_instance.results()
                        # print(f"output of model {model}\n", dictMeasure2dict(data))
                        self.db.set_output(model, data)
                        log("DEBUG", f"{self.name} - {model}: done.")
                        # print("DIZIONARIO DATABANK OUTPUT", self.output)
                        return True
                    except Exception as e:
                        log('ERROR', f"{self.name} - {model}: error while computing: {e}")
                        return None
                except Exception as e:
                    log('ERROR', f"{self.name} - {model}: error while instantiating: {e}")
                    return None
            except KeyError:
                log('ERROR', f"{self.name} - {model}: no class defined!")
                return None
        else:
            log('ERROR', f"{self.name} - {model}: some input is missing")
            return None

    def run_model(self, model):
        if self.compute(model):
            model_output = self.db.get_output(model)
            self.db.set_output(model, model_output)
            return True
        else:
            log("ERROR",f"{model}: uh! Oh! Something went wrong!")
            return False

    def run(self):
        return True
