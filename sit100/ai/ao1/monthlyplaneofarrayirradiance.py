# Arancione SOLE 7 radiazione solare mensile sul piano dei moduli
# input: radiazione solare giornaliera media mensile sul piano dei moduli, mese per mese
import json

from .concept import Measure, MeasureDerivation, ClimatePosition, months
from .utils import log


class MonthlyPlaneOfArrayIrradiance(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_avg_daily_array_irradiance': the_input_data['monthly_avg_daily_array_irradiance'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'monthly_plane_of_array_irradiance': {}
        }

    def validate(self):
        if self.input['monthly_avg_daily_array_irradiance'] is None:
            return False
        entries_number = len(self.input['monthly_avg_daily_array_irradiance'])
        if len(self.input['monthly_avg_daily_array_irradiance']) != 12:
            log("ERROR", f"monthly_avg_daily_array_irradiance must have 12 entries, got {entries_number}")
            print(self.input['monthly_avg_daily_array_irradiance'])
            return False
        for key, val in self.input['monthly_avg_daily_array_irradiance'].items():
            if not isinstance(val, Measure):
                log("ERROR", f"monthly_avg_daily_array_irradiance of {key} must be an instance of Measure")
                return False
        return True

    def compute(self):
        monthly_plane_of_array_irradiance = {}
        for the_month, days in months.items():
            month_avg_array_irradiance = self.input['monthly_avg_daily_array_irradiance'][the_month].value
            month_irradiance = round(month_avg_array_irradiance * days, 2)
            monthly_plane_of_array_irradiance[the_month] = Measure("MWh/mq", month_irradiance)
        self.output['monthly_plane_of_array_irradiance'] = monthly_plane_of_array_irradiance


if __name__ == '__main__':
    irradianza_str = '''{
        "Provincia": "AG",
        "GEN": {
            "Diffuso": "7.1",
            "Diretto": "3.0"
        },
        "FEB": {
            "Diffuso": "7.9",
            "Diretto": "4.3"
        },
        "MAR": {
            "Diffuso": "8.4",
            "Diretto": "7.8"
        },
        "APR": {
            "Diffuso": "8.9",
            "Diretto": "10.1"
        },
        "MAG": {
            "Diffuso": "8.9",
            "Diretto": "14.9"
        },
        "GIU": {
            "Diffuso": "8.4",
            "Diretto": "15.4"
        },
        "LUG": {
            "Diffuso": "9.1",
            "Diretto": "15.6"
        },
        "AGO": {
            "Diffuso": "10.1",
            "Diretto": "12.4"
        },
        "SET": {
            "Diffuso": "10.0",
            "Diretto": "8.8"
        },
        "OTT": {
            "Diffuso": "9.5",
            "Diretto": "5.0"
        },
        "NOV": {
            "Diffuso": "7.9",
            "Diretto": "2.6"
        },
        "DIC": {
            "Diffuso": "6.7",
            "Diretto": "1.6"
        }
    }'''
    irradianza = json.loads(irradianza_str)
    irradianza_tot = {}
    for month in months:
        irtot = (float(irradianza[month]["Diffuso"]) + float(irradianza[month]["Diretto"]))/3.6
        irradianza_tot[month] = Measure("MWh/m2/mese", irtot)
    the_target = MonthlyPlaneOfArrayIrradiance({
        "monthly_avg_daily_array_irradiance": irradianza_tot
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
