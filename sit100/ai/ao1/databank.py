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

import os
import importlib
from .utils import log
from .concept import dict2text, dictMeasure2dict, months
from datetime import datetime

'''
notToImport = ['concept', 'utils', 'databank', 'pipelinesole10349', 'pipeline', 'pipeline2']
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith('.py') and file[:-3] not in notToImport:
        importlib.import_module(f'.{file[:-3]}', 'ao1')
'''


class DataBank:

    def __init__(self, user_data):
        self.input = {}
        self.output = {"UserData": user_data}

    def get_input(self, model):
        if model in self.input:
            return self.input[model]
        else:
            return None

    def set_input(self, model, input_data):
        self.input[model] = input_data
        log('DEBUG', f"input for {model}: {dict2text(input_data, True)}")

    def compute(self, model):
        log("DEBUG", f"DataBank: now computing model {model}")
        if model in self.input:
            in_data = self.get_input(model)
            # print(f"dati di input di {model}", in_data)
            try:
                model_class = globals()[model]
                try:
                    model_instance = model_class(in_data)
                    try:
                        now = datetime.now()
                        log("DEBUG", f"{now} - {model} - validating...")
                        model_instance.validate()
                        log("DEBUG", f"{now} - {model} - computing...")
                        model_instance.compute()
                        # log: info: input ed output del modello
                        data = model_instance.results()
                        # print(f"output of model {model}\n", dictMeasure2dict(data))
                        self.set_output(model, data)
                        log("DEBUG", f"{now} - {model} - done.")
                        # print("DIZIONARIO DATABANK OUTPUT", self.output)
                        return True
                    except Exception as e:
                        log('ERROR', f"error computing model {model}: {e}")
                        return None
                except Exception as e:
                    log('ERROR', f"error instantiating model {model}: {e}")
                    return None
            except KeyError:
                log('ERROR', f"no Class for model: {model}")
                return None
        else:
            log('ERROR', f"input missing for model: {model}")
            return None

    def set_output(self, model, data):
        self.output[model] = data
        log('DEBUG', f"output of {model}: {dict2text(data, True)}")

    def get_output(self, model=None):
        if model is None:
            return self.output
        if model in self.output:
            return self.output[model]
        else:
            return None

    def get_model_output(self, model, unit=False):
        if model in self.output:
            return dictMeasure2dict(self.output[model], unit)
        else:
            log('WARNING', f"DataBank.get_model_output() says: no output for model: {model}")
            return None

    def get_model_type(self, model):
        model_output = self.get_model_output(model)
        if model_output is None:
            return None
        if isinstance(model_output, dict):
            if len(model_output)==1:
                return "single_valued"
            if len(model_output) == 12 and all(month in model_output for month in months):
                return "monthly_valued"
            if all(isinstance(value, (dict, float, int, str)) for value in model_output.values()):
                return "multi_valued"
        return "other"

    def get_output_json(self, model=None):
        if model is None:
            return {model: self.output[model].json() for model in self.output}
        return self.output[model].json()

    def get_output_text(self, model=None):
        def get_output_model_text(the_model):
            return the_model + "\n" + "\n".join([self.output[the_model].text() for the_model in self.output])

        if model is None:
            output_text = ""
            for model in self.output:
                output_text += get_output_model_text(model)
            return output_text
        return get_output_model_text(model)

    def get_text(self, model, unit=True):
        text = ""
        for model, model_data in self.output.items():
            text += dict2text(model_data, unit=unit)
        return text
