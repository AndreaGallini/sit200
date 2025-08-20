# ARCOBALENO 2 Classificazione dei valori di irradiazione solare giornaliera media mensile sul piano dei moduli
import math
from .concept import Measure, MeasureDerivation, months, Classification
from .utils import log


class MonthlyAvgDailyArrayIrradianceClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        the_classes = [
            (3.5, "Molto Bassa"),
            (4.5, "Media"),
            (6.0, "Alta"),
            (7.5, "Molto alta")
            ]
        self.classification = Classification(the_classes)
        try:
            self.input = {
                'monthly_avg_daily_array_irradiance':
                    the_input_data['monthly_avg_daily_array_irradiance']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'monthly_avg_daily_array_irradiance_classification': {
                month: (Measure("", 0), "") for month in months
            }
        }

    def validate(self):
        monthly_avg_daily_array_irradiance = self.input['monthly_avg_daily_array_irradiance']
        if not isinstance(monthly_avg_daily_array_irradiance, dict):
            log("ERROR", "MonthlyAvgIrradianceClassification: monthly_avg_daily_array_irradiance is not a dict")
            return False
        for month in months:
            if month not in monthly_avg_daily_array_irradiance:
                log("ERROR", f"MonthlyAvgIrradianceClassification: missing month {month}")
                return False
            if not isinstance(monthly_avg_daily_array_irradiance[month], Measure):
                log("ERROR", f"MonthlyAvgIrradianceClassification: month {month} value is not a Measure")
                return False
            if not isinstance(monthly_avg_daily_array_irradiance[month].value, (int, float)):
                log("ERROR", "MonthlyAvgIrradianceClassification: month {month} value is not a number")
                return False
        return True

    def compute(self):
        for month in months:
            monthly_avg_daily_array_irradiance = self.input['monthly_avg_daily_array_irradiance'][month]
            the_class = self.classification.classify(monthly_avg_daily_array_irradiance)
            self.output['monthly_avg_daily_array_irradiance_classification'][month] = {
                "monthly_avg_daily_array_irradiance_classification_value": monthly_avg_daily_array_irradiance.value,
                "monthly_avg_daily_array_irradiance_classification_unit": monthly_avg_daily_array_irradiance.unit,
                "monthly_avg_daily_array_irradiance_classification_threshold_value": the_class[0],
                "monthly_avg_daily_array_irradiance_classification_threshold_name": the_class[1]
            }

    def get_text(self):
        results = "Monthly Average Daily Irradiance on the plane of the array:\n"
        for month in months:
            month_result = self.output['monthly_avg_daily_array_irradiance_classification'][month]
            the_value = month_result["monthly_avg_daily_array_irradiance_classification_value"]
            the_unit = month_result["monthly_avg_daily_array_irradiance_classification_unit"]
            # threshold_value = month_result["monthly_avg_daily_array_irradiance_classification_threshold_value"]
            the_class_name = month_result["monthly_avg_daily_array_irradiance_classification_threshold_name"]
            results += f"\t{month}: {the_value:.2f} {the_unit} {the_class_name}\n"
        return results


if __name__ == '__main__':
    the_target = MonthlyAvgDailyArrayIrradianceClassification({
        "monthly_avg_daily_array_irradiance":
            {
                "GEN": Measure("kWh/m2/giorno", 2.70),
                "FEB": Measure("kWh/m2/giorno", 4.10),
                "MAR": Measure("kWh/m2/giorno", 2.41),
                "APR": Measure("kWh/m2/giorno", 1.53),
                "MAG": Measure("kWh/m2/giorno", 2.00),
                "GIU": Measure("kWh/m2/giorno", 6.27),
                "LUG": Measure("kWh/m2/giorno", 3.65),
                "AGO": Measure("kWh/m2/giorno", 5.50),
                "SET": Measure("kWh/m2/giorno", 4.60),
                "OTT": Measure("kWh/m2/giorno", 6.66),
                "NOV": Measure("kWh/m2/giorno", 5.70),
                "DIC": Measure("kWh/m2/giorno", 8.94)
            }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.get_text())
    else:
        print("input not valid, error")
