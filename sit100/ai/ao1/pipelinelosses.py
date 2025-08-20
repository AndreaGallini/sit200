from .concept import Measure, dictMeasure2dict, months
from .databank import DataBank
from .utils import log
from .pipeline import Pipeline


class PipelineLosses(Pipeline):
    def __init__(self, db: DataBank):
        expected_data = {
            "shading_obstacle": "%",
            "shading_horizon": "%",
            "tilt": "°"
        }
        super().__init__(db, expected_data)

    def run(self):
        # ARANCIONE ITE 1a perdite per temperatura sistema fisso
        monthly_avg_daily_temperature = self.db.get_output('MonthlyAvgDailyTemperature')
        self.db.set_input("FixedSysMonthlyTempLoss", {
            "monthly_avg_daily_temperature": monthly_avg_daily_temperature['monthly_avg_daily_temperature']
        })
        if self.db.compute("FixedSysMonthlyTempLoss"):
            fixed_sys_monthly_temp_loss = self.db.get_output("FixedSysMonthlyTempLoss")
            self.db.set_output("FixedSysMonthlyTempLoss", fixed_sys_monthly_temp_loss)
        else:
            log("ERROR", "MonthlyAvgDailyTemperature: uh! Oh! Something went wrong!")
            return False

        # ARANCIONE ITE 1c perdite per temperatura formula empirica fisso
        self.db.set_input("FixedSysMonthlyEmpiricalTempLoss", {})
        if self.db.compute("FixedSysMonthlyEmpiricalTempLoss"):
            fixed_sys_empirical_temp_loss = self.db.get_output("FixedSysMonthlyEmpiricalTempLoss")
            self.db.set_output("FixedSysMonthlyEmpiricalTempLoss", fixed_sys_empirical_temp_loss)
        else:
            log("ERROR", "FixedSysMonthlyEmpiricalTempLoss: uh! Oh! Something went wrong!")
            return False

        # ARANCIONE ITE 2 perdite per riflessione
        self.db.set_input("FixedSysMonthlyReflectionLoss", {})
        if self.db.compute("FixedSysMonthlyReflectionLoss"):
            fixed_sys_monthly_reflection_loss = self.db.get_output("FixedSysMonthlyReflectionLoss")
            self.db.set_output("FixedSysMonthlyReflectionLoss", fixed_sys_monthly_reflection_loss)
        else:
            log("ERROR","FixedSysMonthlyReflectionLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 3 perdite per sporcamento
        tilt = self.db.get_output("UserData")["tilt"]
        self.db.set_input("FixedSysMonthlySoilingLoss", {"tilt": tilt})
        if self.db.compute("FixedSysMonthlySoilingLoss"):
            fixed_sys_monthly_soiling_loss = self.db.get_output("FixedSysMonthlySoilingLoss")
            self.db.set_output("FixedSysMonthlySoilingLoss", fixed_sys_monthly_soiling_loss)
        else:
            log("ERROR", "FixedSysMonthlySoilingLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 4 perdite per liv. di irraggiamento
        theoretical_annual_yield = self.db.get_output("TheoreticalAnnualYield")  # ARANCIONE SOLE 9
        self.db.set_input("FixedSysMonthlyLowIrradianceLoss", theoretical_annual_yield)
        if self.db.compute("FixedSysMonthlyLowIrradianceLoss"):
            fixed_sys_monthly_low_irradiance_loss = self.db.get_output("FixedSysMonthlyLowIrradianceLoss")
            self.db.set_output("FixedSysMonthlyLowIrradianceLoss", fixed_sys_monthly_low_irradiance_loss)
        else:
            log("ERROR", "FixedSysMonthlyLowIrradianceLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 5 perdite per mismatching
        self.db.set_input("FixedSysMonthlyMismatchingLoss", {})
        if self.db.compute("FixedSysMonthlyMismatchingLoss"):
            fixed_sys_monthly_mismatching_loss = self.db.get_output("FixedSysMonthlyMismatchingLoss")
            self.db.set_output("FixedSysMonthlyMismatchingLoss", fixed_sys_monthly_mismatching_loss)
        else:
            log("ERROR", "FixedSysMonthlyMismatchingLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 6 perdite nei cavi o perdite ohmiche
        self.db.set_input("FixedSysMonthlyCableLoss", {})
        if self.db.compute("FixedSysMonthlyCableLoss"):
            fixed_sys_monthly_cable_loss = self.db.get_output("FixedSysMonthlyCableLoss")
            self.db.set_output("FixedSysMonthlyCableLoss", fixed_sys_monthly_cable_loss)
        else:
            log("ERROR", "FixedSysMonthlyCableLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 7 perdite inverter
        self.db.set_input("FixedSysMonthlyInverterLoss", {
            "european_inverter_efficiency": Measure("%", 97.0)
        })
        if self.db.compute("FixedSysMonthlyInverterLoss"):
            fixed_sys_monthly_inverter_loss = self.db.get_output("FixedSysMonthlyInverterLoss")
            self.db.set_output("FixedSysMonthlyInverterLoss", fixed_sys_monthly_inverter_loss)
        else:
            log("ERROR", "FixedSysMonthlyInverterLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 8 altre perdite di sistema
        self.db.set_input("FixedSysMonthlyOtherLoss", {})
        if self.db.compute("FixedSysMonthlyOtherLoss"):
            fixed_sys_monthly_other_loss = self.db.get_output("FixedSysMonthlyOtherLoss")
            self.db.set_output("FixedSysMonthlyOtherLoss", fixed_sys_monthly_other_loss)
        else:
            log("ERROR", "FixedSysMonthlyOtherLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 9d Ombreggiamento ostacoli
        shading_obstacle = self.db.get_output("UserData")["shading_obstacle"]
        self.db.set_input("FixedSysMonthlyObstacleShading", {
            "shading_obstacle": shading_obstacle
        })
        if self.db.compute("FixedSysMonthlyObstacleShading"):
            fixed_sys_monthly_obstacle_shading = self.db.get_output("FixedSysMonthlyObstacleShading")
            self.db.set_output("FixedSysMonthlyObstacleShading", fixed_sys_monthly_obstacle_shading)
        else:
            log("ERROR", "FixedSysMonthlyObstacleShading: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 9e Ombreggiamento clinometrico
        shading_horizon = self.db.get_output("UserData")["shading_horizon"]
        self.db.set_input("FixedSysMonthlyClinometricShading", {
            "shading_horizon": shading_horizon
        })
        if self.db.compute("FixedSysMonthlyClinometricShading"):
            fixed_sys_monthly_clinometric_shading = self.db.get_output("FixedSysMonthlyClinometricShading")
            self.db.set_output("FixedSysMonthlyClinometricShading", fixed_sys_monthly_clinometric_shading)
        else:
            log("ERROR", "FixedSysMonthlyClinometricShading: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 9f perdita percentuale da ombreggiamento
        self.db.set_input("FixedSysMonthlyShadingLossPercentage", {
            "fixed_sys_monthly_obstacle_shading": fixed_sys_monthly_obstacle_shading[
                'fixed_sys_monthly_obstacle_shading'],
            "fixed_sys_monthly_clinometric_shading": fixed_sys_monthly_clinometric_shading[
                'fixed_sys_monthly_clinometric_shading']
        })
        if self.db.compute("FixedSysMonthlyShadingLossPercentage"):
            fixed_sys_monthly_shading_loss_percentage = self.db.get_output("FixedSysMonthlyShadingLossPercentage")
            self.db.set_output("FixedSysMonthlyShadingLossPercentage", fixed_sys_monthly_shading_loss_percentage)
        else:
            log("ERROR", "FixedSysMonthlyShadingLossPercentage: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 10 perdita da ombreggiamento
        monthly_plane_of_array_irradiance = self.db.get_output("MonthlyPlaneOfArrayIrradiance")
        self.db.set_input("FixedSysMonthlyShadingLoss", {
            "fixed_sys_monthly_shading_loss_percentage": fixed_sys_monthly_shading_loss_percentage[
                'fixed_sys_monthly_shading_loss_percentage'],
            "monthly_plane_of_array_irradiance": monthly_plane_of_array_irradiance[
                'monthly_plane_of_array_irradiance']
        })
        if self.db.compute("FixedSysMonthlyShadingLoss"):
            fixed_sys_monthly_shading_loss = self.db.get_output("FixedSysMonthlyShadingLoss")
            self.db.set_output("FixedSysMonthlyShadingLoss", fixed_sys_monthly_shading_loss)
        else:
            log("ERROR", "FixedSysMonthlyShadingLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 11 energia persa annua per ombreggiamento
        self.db.set_input("FixedSysAnnualShadingLoss", {
            "fixed_sys_monthly_shading_loss": fixed_sys_monthly_shading_loss["fixed_sys_monthly_shading_loss"]
        })
        if self.db.compute("FixedSysAnnualShadingLoss"):
            fixed_sys_annual_shading_loss = self.db.get_output("FixedSysAnnualShadingLoss")
            self.db.set_output("FixedSysAnnualShadingLoss", fixed_sys_annual_shading_loss)
        else:
            log("ERROR", "FixedSysAnnualShadingLoss: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 12 Riassunto perdite di sistema per mese (8 tipologie) - escluso ombreggiamento
        self.db.set_input("MonthlySystemLossesSummary", {
            'fixed_sys_monthly_temp_loss': fixed_sys_monthly_temp_loss['fixed_sys_monthly_temp_loss'],
            'fixed_sys_monthly_reflection_loss': fixed_sys_monthly_reflection_loss['fixed_sys_monthly_reflection_loss'],
            'fixed_sys_monthly_soiling_loss': fixed_sys_monthly_soiling_loss['fixed_sys_monthly_soiling_loss'],
            'fixed_sys_monthly_low_irradiance_loss': fixed_sys_monthly_low_irradiance_loss[
                'fixed_sys_monthly_low_irradiance_loss'],
            'fixed_sys_monthly_mismatching_loss': fixed_sys_monthly_mismatching_loss[
                'fixed_sys_monthly_mismatching_loss'],
            'fixed_sys_monthly_cable_loss': fixed_sys_monthly_cable_loss['fixed_sys_monthly_cable_loss'],
            'fixed_sys_monthly_inverter_loss': fixed_sys_monthly_inverter_loss['fixed_sys_monthly_inverter_loss'],
            'fixed_sys_monthly_other_loss': fixed_sys_monthly_other_loss['fixed_sys_monthly_other_loss'],
        })
        if self.db.compute("MonthlySystemLossesSummary"):
            monthly_system_efficiency_summary = self.db.get_output("MonthlySystemLossesSummary")
            self.db.set_output("MonthlySystemLossesSummary", monthly_system_efficiency_summary)
        else:
            log("ERROR", "MonthlySystemLossesSummary: uh! Oh! Something went wrong!")
            return False

        # Arancione ITE 13 Riassunto efficienze di sistema per mese (8 tipologie) - escluso ombreggiamento
        self.db.set_input("MonthlySystemEfficiencySummary", {
            'fixed_sys_monthly_temp_loss': fixed_sys_monthly_temp_loss['fixed_sys_monthly_temp_loss'],
            'fixed_sys_monthly_reflection_loss': fixed_sys_monthly_reflection_loss['fixed_sys_monthly_reflection_loss'],
            'fixed_sys_monthly_soiling_loss': fixed_sys_monthly_soiling_loss['fixed_sys_monthly_soiling_loss'],
            'fixed_sys_monthly_low_irradiance_loss': fixed_sys_monthly_low_irradiance_loss[
                'fixed_sys_monthly_low_irradiance_loss'],
            'fixed_sys_monthly_mismatching_loss': fixed_sys_monthly_mismatching_loss[
                'fixed_sys_monthly_mismatching_loss'],
            'fixed_sys_monthly_cable_loss': fixed_sys_monthly_cable_loss['fixed_sys_monthly_cable_loss'],
            'fixed_sys_monthly_inverter_loss': fixed_sys_monthly_inverter_loss['fixed_sys_monthly_inverter_loss'],
            'fixed_sys_monthly_other_loss': fixed_sys_monthly_other_loss['fixed_sys_monthly_other_loss'],
        })
        if self.db.compute("MonthlySystemEfficiencySummary"):
            monthly_system_efficiency_summary = self.db.get_output("MonthlySystemEfficiencySummary")
            self.db.set_output("MonthlySystemEfficiencySummary", monthly_system_efficiency_summary)
        else:
            log("ERROR", "MonthlySystemEfficiencySummary: uh! Oh! Something went wrong!")
            return False


        return True
