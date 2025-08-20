# RED E6E Average monthly power production
from concept import Measure, MeasureDerivation
import os.path
import matplotlib.pyplot as plt


class AverageMonthlyPowerProduction(MeasureDerivation):
    def __init__(self, data_file, the_input_data=None):
        if not os.path.exists(data_file):
            raise Exception("No average solar radiation data found.")
        self.monthly_solar_radiation = {}
        with open(data_file, newline="") as csvfile:
            next(csvfile)
            for row in csvfile:
                month, value = row.strip().split(";")
                self.monthly_solar_radiation[month] = float(value)
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                "system_loss": the_input_data["system_loss"],
                "power_peak": the_input_data["power_peak"],
                "module_efficiency": the_input_data["module_efficiency"],
                "inverter_efficiency": the_input_data["inverter_efficiency"],
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "monthly_energy_production": {}
        }

    def compute(self):
        monthly_usable_radiation = {}
        monthly_energy_production = {}
        for x in self.monthly_solar_radiation.items():
            monthly_usable_radiation[x[0]] = x[1] * (1-self.input["system_loss"].value/100)
            monthly_energy_production[x[0]] = (
                    self.input['power_peak'].value
                    * monthly_usable_radiation[x[0]]
                    * self.input['inverter_efficiency'].value / 100
                    * self.input['module_efficiency'].value / 100
            )
            self.output["monthly_energy_production"][x[0]] = Measure("kWh", monthly_energy_production[x[0]])


if __name__ == '__main__':
    the_target = AverageMonthlyPowerProduction(
        "average_solar_radiation.csv",
        {
            "system_loss": Measure("%", 27.0),
            "power_peak": Measure("kW", 3.0),
            "module_efficiency": Measure("%", 19.0),
            "inverter_efficiency": Measure("%", 97.0),
        }
    )
    the_target.main()
    print(the_target.dump())
    months = the_target.output['monthly_energy_production'].keys()
    production_monthly_measures = the_target.output['monthly_energy_production'].values()
    production_monthly = [x.value for x in production_monthly_measures]
    plt.figure(figsize=(10, 6))
    plt.bar(months, production_monthly, color='skyblue')
    plt.xlabel('Mesi dell\'Anno')
    plt.ylabel('Produzione Elettrica Media Mensile (kWh)')
    plt.title('Produzione Elettrica Media Mensile di un Impianto Fotovoltaico a Roma')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
