from .databank import DataBank
from .pipeline import Pipeline
from .utils import log


class PipelineEnergy(Pipeline):
    def __init__(self, db: DataBank):
        expected_data = {
            "nominal_peak_power": "kWp"
        }
        super().__init__(db, expected_data)

    def run(self):
        # Arancione EE 1 Energia utile mensile	MonthlyNetEnergy
        monthly_plane_of_array_irradiance = self.db.get_output("MonthlyPlaneOfArrayIrradiance")
        fixed_sys_monthly_shading_loss = self.db.get_output("FixedSysMonthlyShadingLoss")
        self.db.set_input("MonthlyNetEnergy", {
            "monthly_plane_of_array_irradiance": monthly_plane_of_array_irradiance[
                "monthly_plane_of_array_irradiance"],
            "fixed_sys_monthly_shading_loss": fixed_sys_monthly_shading_loss["fixed_sys_monthly_shading_loss"]
        })
        if self.db.compute("MonthlyNetEnergy"):
            monthly_net_energy = self.db.get_output("MonthlyNetEnergy")
            self.db.set_output("MonthlyNetEnergy", monthly_net_energy)
        else:
            log("ERROR", "MonthlyNetEnergy: uh! Oh! Something went wrong!")
            return False

        # Arancione EE 2 Energia utile annua (kWh/mq)	AnnualNetEnergy
        annual_solar_radiation = self.db.get_output("AnnualSolarRadiation")
        fixed_sys_annual_shading_loss = self.db.get_output("FixedSysAnnualShadingLoss")
        self.db.set_input("AnnualNetEnergy", {
            "annual_solar_radiation": annual_solar_radiation["annual_solar_radiation"],
            "fixed_sys_annual_shading_loss": fixed_sys_annual_shading_loss["fixed_sys_annual_shading_loss"]
        })
        if self.db.compute("AnnualNetEnergy"):
            monthly_net_energy = self.db.get_output("AnnualNetEnergy")
            self.db.set_output("AnnualNetEnergy", monthly_net_energy)
        else:
            log("ERROR", "AnnualNetEnergy: uh! Oh! Something went wrong!")
            return False

        # Arancione EE 3 Efficienza percentuale mensile di sistema	MonthlyEfficiencyPercentage
        fixed_sys_monthly_temp_loss = self.db.get_output("FixedSysMonthlyTempLoss")
        fixed_sys_monthly_reflection_loss = self.db.get_output("FixedSysMonthlyReflectionLoss")
        fixed_sys_monthly_soiling_loss = self.db.get_output("FixedSysMonthlySoilingLoss")
        fixed_sys_monthly_low_irradiance_loss = self.db.get_output("FixedSysMonthlyLowIrradianceLoss")
        fixed_sys_monthly_mismatching_loss = self.db.get_output("FixedSysMonthlyMismatchingLoss")
        fixed_sys_monthly_cable_loss = self.db.get_output("FixedSysMonthlyCableLoss")
        fixed_sys_monthly_inverter_loss = self.db.get_output("FixedSysMonthlyInverterLoss")
        fixed_sys_monthly_other_loss = self.db.get_output("FixedSysMonthlyOtherLoss")
        self.db.set_input("MonthlyEfficiencyPercentage", {
            "fixed_sys_monthly_temp_loss": fixed_sys_monthly_temp_loss["fixed_sys_monthly_temp_loss"],
            "fixed_sys_monthly_reflection_loss": fixed_sys_monthly_reflection_loss["fixed_sys_monthly_reflection_loss"],
            "fixed_sys_monthly_soiling_loss": fixed_sys_monthly_soiling_loss["fixed_sys_monthly_soiling_loss"],
            "fixed_sys_monthly_low_irradiance_loss": fixed_sys_monthly_low_irradiance_loss[
                "fixed_sys_monthly_low_irradiance_loss"],
            "fixed_sys_monthly_mismatching_loss": fixed_sys_monthly_mismatching_loss[
                "fixed_sys_monthly_mismatching_loss"],
            "fixed_sys_monthly_cable_loss": fixed_sys_monthly_cable_loss["fixed_sys_monthly_cable_loss"],
            "fixed_sys_monthly_inverter_loss": fixed_sys_monthly_inverter_loss["fixed_sys_monthly_inverter_loss"],
            "fixed_sys_monthly_other_loss": fixed_sys_monthly_other_loss["fixed_sys_monthly_other_loss"]
        })
        if self.db.compute("MonthlyEfficiencyPercentage"):
            monthly_efficiency_percentage = self.db.get_output("MonthlyEfficiencyPercentage")
            self.db.set_output("MonthlyEfficiencyPercentage", monthly_efficiency_percentage)
        else:
            log("ERROR", "MonthlyEfficiencyPercentage: uh! Oh! Something went wrong!")
            return False

        # Arancione EE 4 Producibilità mensile	MonthlyEnergyYield
        monthly_net_energy = self.db.get_output("MonthlyNetEnergy")
        monthly_efficiency_percentage = self.db.get_output("MonthlyEfficiencyPercentage")
        self.db.set_input("MonthlyEnergyYield", {
            "monthly_net_energy": monthly_net_energy['monthly_net_energy'],
            "monthly_efficiency_percentage": monthly_efficiency_percentage['monthly_efficiency_percentage']
        })
        if self.db.compute("MonthlyEnergyYield"):
            monthly_efficiency_percentage = self.db.get_output("MonthlyEnergyYield")
            self.db.set_output("MonthlyEnergyYield", monthly_efficiency_percentage)
        else:
            log("ERROR", "MonthlyEnergyYield: uh! Oh! Something went wrong!")
            return False

        # Arancione EE 5 Producibilità annua. AnnualEnergyYield
        monthly_energy_yield = self.db.get_output("MonthlyEnergyYield")
        self.db.set_input("AnnualEnergyYield", {
            "monthly_energy_yield": monthly_energy_yield['monthly_energy_yield']
        })
        if self.db.compute("AnnualEnergyYield"):
            monthly_efficiency_percentage = self.db.get_output("AnnualEnergyYield")
            self.db.set_output("AnnualEnergyYield", monthly_efficiency_percentage)
        else:
            log("ERROR", "AnnualEnergyYield: uh! Oh! Something went wrong!")
            return False

        # Arancione EE 6 Efficienza di sistema.	SystemEfficiency
        annual_net_energy = self.db.get_output("AnnualNetEnergy")
        annual_energy_yield = self.db.get_output("AnnualEnergyYield")
        self.db.set_input("SystemEfficiency", {
            "annual_net_energy": annual_net_energy['annual_net_energy'],
            "annual_energy_yield": annual_energy_yield['annual_energy_yield']
        })
        if self.db.compute("SystemEfficiency"):
            monthly_efficiency_percentage = self.db.get_output("SystemEfficiency")
            self.db.set_output("SystemEfficiency", monthly_efficiency_percentage)
        else:
            log("ERROR", "SystemEfficiency: uh! Oh! Something went wrong!")
            return False

        # Arancione EE 7 Producibilità giornaliera media giorno	DailyAvgEnergyYield
        monthly_energy_yield = self.db.get_output("MonthlyEnergyYield")
        self.db.set_input("DailyAvgEnergyYield", {
            "monthly_energy_yield": monthly_energy_yield['monthly_energy_yield']
        })
        if self.db.compute("DailyAvgEnergyYield"):
            daily_energy_yield = self.db.get_output("DailyAvgEnergyYield")
            self.db.set_output("DailyAvgEnergyYield", daily_energy_yield)
        else:
            log("ERROR", "DailyAvgEnergyYield: uh! Something went wrong!")
            return False

        # Arancione EE 8 Producibilità giornaliera media annua	DailyEnergyYield
        annual_energy_yield = self.db.get_output("AnnualEnergyYield")
        self.db.set_input("DailyEnergyYield", {
            "annual_energy_yield": annual_energy_yield['annual_energy_yield']
        })
        if self.db.compute("DailyEnergyYield"):
            daily_energy_yield = self.db.get_output("DailyEnergyYield")
            self.db.set_output("DailyEnergyYield", daily_energy_yield)
        else:
            log("ERROR", "DailyEnergyYield: uh! Something went wrong!")
            return False

        # Arancione EE 9 Produzione energia elettrica media mensile MonthlyAvgEnergyProduction
        monthly_energy_yield = self.db.get_output("MonthlyEnergyYield")
        nominal_peak_power = self.db.get_output("UserData")
        self.db.set_input("MonthlyAvgEnergyProduction", {
            "monthly_energy_yield": monthly_energy_yield['monthly_energy_yield'],
            "nominal_peak_power": nominal_peak_power['nominal_peak_power']
        })
        if self.db.compute("MonthlyAvgEnergyProduction"):
            monthly_avg_energy_production = self.db.get_output("MonthlyAvgEnergyProduction")
            self.db.set_output("MonthlyAvgEnergyProduction", monthly_avg_energy_production)
        else:
            log("ERROR", "MonthlyAvgEnergyProduction: uh! Something went wrong!")
            return False

        # Arancione EE 10 Produzione energia elettrica annua (kWh/anno)	AnnualEnergyProduction
        monthly_avg_energy_production = self.db.get_output("MonthlyAvgEnergyProduction")
        self.db.set_input("AnnualEnergyProduction", {
            "monthly_avg_energy_production": monthly_avg_energy_production['monthly_avg_energy_production']
        })
        if self.db.compute("AnnualEnergyProduction"):
            annual_energy_production = self.db.get_output("AnnualEnergyProduction")
            self.db.set_output("AnnualEnergyProduction", annual_energy_production)
        else:
            log("ERROR", "AnnualEnergyProduction: uh! Something went wrong!")
            return False

        # Arancione EE 11 perdita annua percentuale AnnualLossPercentage
        theoretical_annual_yield = self.db.get_output("TheoreticalAnnualYield")
        annual_energy_yield = self.db.get_output("AnnualEnergyYield")
        self.db.set_input("AnnualLossPercentage", {
            "theoretical_annual_yield": theoretical_annual_yield['theoretical_annual_yield'],
            "annual_energy_yield": annual_energy_yield['annual_energy_yield']
        })
        if self.db.compute("AnnualLossPercentage"):
            annual_loss_percentage = self.db.get_output("AnnualLossPercentage")
            self.db.set_output("AnnualLossPercentage", annual_loss_percentage)
        else:
            log("ERROR", "AnnualLossPercentage: uh! Something went wrong!")
            return False

        # Arcobaleno 3 classificazione del valore di perdita % totale di sistema AnnualLossPercentageClassification
        annual_loss_percentage = self.db.get_output("AnnualLossPercentage")
        self.db.set_input("AnnualLossPercentageClassification", {
            "annual_loss_percentage": annual_loss_percentage['annual_loss_percentage']
        })
        if self.db.compute("AnnualLossPercentageClassification"):
            annual_loss_percentage_classification = self.db.get_output("AnnualLossPercentageClassification")
            self.db.set_output("AnnualLossPercentageClassification", annual_loss_percentage_classification)
        else:
            log("ERROR", "AnnualLossPercentageClassification: uh! Something went wrong!")
            return False

        # Arcobaleno 4 classificazione del valore di energia utile annua AnnualNetEnergyClassification
        annual_net_energy = self.db.get_output("AnnualNetEnergy")
        self.db.set_input("AnnualNetEnergyClassification", {
            "annual_net_energy": annual_net_energy['annual_net_energy']
        })
        if self.db.compute("AnnualNetEnergyClassification"):
            annual_net_energy_classification = self.db.get_output("AnnualNetEnergyClassification")
            self.db.set_output("AnnualNetEnergyClassification", annual_net_energy_classification)
        else:
            log("ERROR", "AnnualNetEnergyClassification: uh! Something went wrong!")
            return False

        # Arcobaleno 5 classificazione del valore di efficienza percentuale del sistema SystemEfficiencyClassification
        system_efficiency = self.db.get_output("SystemEfficiency")
        self.db.set_input("SystemEfficiencyClassification", {
            "system_efficiency": system_efficiency['system_efficiency']
        })
        if self.db.compute("SystemEfficiencyClassification"):
            system_efficiency_classification = self.db.get_output("SystemEfficiencyClassification")
            self.db.set_output("SystemEfficiencyClassification", system_efficiency_classification)
        else:
            log("ERROR", "SystemEfficiencyClassification: uh! Something went wrong!")
            return False

        # Arancione RID 1 riduzione GHG
        self.db.set_input("GreenHouseGasesReduction", annual_energy_production)
        if self.db.compute("GreenHouseGasesReduction"):
            greenhouse_gases_reduction = self.db.get_output("GreenHouseGasesReduction")
            self.db.set_output("GreenHouseGasesReduction", greenhouse_gases_reduction)
        else:
            log("ERROR", "GreenHouseGasesReduction: uh! Something went wrong!")
            return False

        # Arancione RID 2 riduzione TEP
        self.db.set_input("TEPReduction", annual_energy_production)
        if self.db.compute("TEPReduction"):
            tep_reduction = self.db.get_output("TEPReduction")
            self.db.set_output("TEPReduction", tep_reduction)
        else:
            log("ERROR", "TEPReduction: uh! Something went wrong!")
            return False

        return True
