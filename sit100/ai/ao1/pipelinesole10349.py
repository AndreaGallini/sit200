from .concept import Measure, dictMeasure2dict
from .databank import DataBank
from .utils import log
from .pipeline import Pipeline


class PipelineSole10349(Pipeline):

    def __init__(self, db: DataBank):
        expected_data = {
            'latitude': "°",
            'longitude': "°",
            'tilt': "°",
            'azimuth': "°",
            'albedo': ""
        }
        super().__init__(db, expected_data)

    def run(self):

        # Arancione SOLE 1 Temperatura giornaliera media mensile
        latitude = self.db.get_output("UserData")["latitude"]
        longitude = self.db.get_output("UserData")["longitude"]
        self.db.set_input("MonthlyAvgDailyTemperature", {
            "latitude": latitude,
            "longitude": longitude
        })
        if not self.run_model("MonthlyAvgDailyTemperature"):
            return False


        # Arancione SOLE 2 Temperatura media annua [°C]
        self.db.set_input("AnnualAvgTemperature", {
            "latitude": latitude,
            "longitude": longitude
        })
        if not self.run_model("AnnualAvgTemperature"):
            return False

        # ARANCIONE SOLE 5a
        self.db.set_input("MonthlyAvgHorizontalIrradianceUni10349", {
            "latitude": latitude,
            "longitude": longitude
        })
        if self.db.compute("MonthlyAvgHorizontalIrradianceUni10349"):
            monthly_avg_daily_horizontal_irradiance = self.db.get_output("MonthlyAvgHorizontalIrradianceUni10349")
            # print(monthly_avg_daily_horizontal_irradiance.keys())
            # for the_k, the_v in monthly_avg_daily_horizontal_irradiance['monthly_avg_daily_horizontal_irradiance'].items():
            #    print(the_k, the_v)
            self.db.set_output("MonthlyAvgHorizontalIrradianceUni10349", monthly_avg_daily_horizontal_irradiance)
        else:
            log("ERROR", "MonthlyAvgHorizontalIrradianceUni10349: uh! Something went wrong!")
            return False

        # ARANCIONE SOLE 6a
        azimuth = self.db.get_output("UserData")["azimuth"]
        tilt = self.db.get_output("UserData")["tilt"]
        albedo = self.db.get_output("UserData")["albedo"]
        monthly_avg_daily_horizontal_irradiance = self.db.get_output("MonthlyAvgHorizontalIrradianceUni10349")
        log("DEBUG", f"{monthly_avg_daily_horizontal_irradiance['monthly_avg_daily_beam_horizontal_irradiance']['GEN'].value}")
        monthly_avg_daily_diffuse_horizontal_irradiance = monthly_avg_daily_horizontal_irradiance[
            'monthly_avg_daily_diffuse_horizontal_irradiance']
        monthly_avg_daily_beam_horizontal_irradiance = monthly_avg_daily_horizontal_irradiance[
            'monthly_avg_daily_beam_horizontal_irradiance']
        monthly_avg_daily_horizontal_irradiance = monthly_avg_daily_horizontal_irradiance[
            'monthly_avg_daily_horizontal_irradiance']
        self.db.set_input("MonthlyAvgDailyArrayIrradianceUni10349", {
            'monthly_avg_daily_diffuse_horizontal_irradiance': monthly_avg_daily_diffuse_horizontal_irradiance,
            'monthly_avg_daily_beam_horizontal_irradiance': monthly_avg_daily_beam_horizontal_irradiance,
            'monthly_avg_daily_horizontal_irradiance': monthly_avg_daily_horizontal_irradiance,
            'latitude': latitude,
            'azimuth': azimuth,
            'tilt': tilt,
            'albedo': albedo
        })
        if self.db.compute("MonthlyAvgDailyArrayIrradianceUni10349"):
            monthly_avg_daily_array_irradiance = self.db.get_output("MonthlyAvgDailyArrayIrradianceUni10349")
            self.db.set_output("MonthlyAvgDailyArrayIrradianceUni10349", monthly_avg_daily_array_irradiance)
        else:
            log("ERROR", "MonthlyAvgDailyArrayIrradianceUni10349: oh no! Something went wrong! ")
            return False

        # ARCOBALENO 2 Classificazione dei valori di irradiazione solare giornaliera media mensile sul piano dei moduli
        self.db.set_input("MonthlyAvgDailyArrayIrradianceClassification",{
            "monthly_avg_daily_array_irradiance":
                monthly_avg_daily_array_irradiance['monthly_avg_daily_array_irradiance']
        })
        if not self.run_model("MonthlyAvgDailyArrayIrradianceClassification"):
            return False


        # Arancione SOLE 7 Radiazione solare mensile sul piano dei moduli
        self.db.set_input('MonthlyPlaneOfArrayIrradiance', monthly_avg_daily_array_irradiance)
        if self.db.compute("MonthlyPlaneOfArrayIrradiance"):
            monthly_plane_of_array_irradiance = self.db.get_output("MonthlyPlaneOfArrayIrradiance")
            self.db.set_output("MonthlyPlaneOfArrayIrradiance", monthly_plane_of_array_irradiance)
        else:
            log("ERROR", "MonthlyPlaneOfArrayIrradiance: uh! Something went wrong! ")
            return False

        # Arancione SOLE 8 Radiazione solare annua sul piano dei moduli
        self.db.set_input("AnnualSolarRadiation", {
            "monthly_plane_of_array_irradiance": monthly_plane_of_array_irradiance["monthly_plane_of_array_irradiance"]
        })
        if self.db.compute("AnnualSolarRadiation"):
            annual_solar_radiation = self.db.get_output("AnnualSolarRadiation")
            self.db.set_output("AnnualSolarRadiation", annual_solar_radiation)
        else:
            log("ERROR", "AnnualSolarRadiation: uh! Something went wrong!")
            return False

        # Arancione SOLE 9 Producibilità annua teorica
        self.db.set_input("TheoreticalAnnualYield", annual_solar_radiation)
        if self.db.compute("TheoreticalAnnualYield"):
            theoretical_annual_yield = self.db.get_output("TheoreticalAnnualYield")
            self.db.set_output("TheoreticalAnnualYield", theoretical_annual_yield)
        else:
            log("ERROR", "TheoreticalAnnualYield: uh! Something went wrong!")
            return False

        # Arancione SOLE 10 Ore di luce al giorno, media mensile
        self.db.set_input("MonthlyAvgDaylightHours", {'latitude': latitude})
        if self.db.compute("MonthlyAvgDaylightHours"):
            monthly_avg_daylight_hours = self.db.get_output("MonthlyAvgDaylightHours")
            self.db.set_output("MonthlyAvgDaylightHours", monthly_avg_daylight_hours)
        else:
            log("ERROR", "MonthlyAvgDaylightHours: uh! Something went wrong!")
            return False

        # Arancione SOLE 11 Ore di luce al giorno, media annuale
        monthly_avg_daylight_hours = self.db.get_output("MonthlyAvgDaylightHours")
        self.db.set_input("AnnualAvgDaylightHours", monthly_avg_daylight_hours)
        if self.db.compute("AnnualAvgDaylightHours"):
            annual_avg_daylight_hours = self.db.get_output("AnnualAvgDaylightHours")
            self.db.set_output("AnnualAvgDaylightHours", annual_avg_daylight_hours)
        else:
            log("ERROR", "AnnualAvgDaylightHours: uh! Something went wrong!")
            return False

        # Arancione SOLE 12 irradiazione solare riflessa giornaliera media mensile sul piano orizzontale
        self.db.set_input("MonthlyAvgDailyHorizontalSolarIrradianceSummary", {
            'monthly_avg_daily_diffuse_horizontal_irradiance': monthly_avg_daily_diffuse_horizontal_irradiance,
            'monthly_avg_daily_beam_horizontal_irradiance': monthly_avg_daily_beam_horizontal_irradiance,
            'monthly_avg_daily_horizontal_irradiance': monthly_avg_daily_horizontal_irradiance,
            'albedo': albedo
        })
        if self.db.compute("MonthlyAvgDailyHorizontalSolarIrradianceSummary"):
            monthly_avg_daily_horizontal_solar_irradiance_summary = self.db.get_output("MonthlyAvgDailyHorizontalSolarIrradianceSummary")
            self.db.set_output("MonthlyAvgDailyHorizontalSolarIrradianceSummary", monthly_avg_daily_horizontal_solar_irradiance_summary)
        else:
            log("ERROR", "MonthlyAvgDailyHorizontalSolarIrradianceSummary: oh no! Something went wrong! ")
            return False

        return True
