# RED E8E monthly specific yield
from concept import Measure, MeasureDerivation
import os.path
import matplotlib.pyplot as plt


class MonthlySpecificYield(MeasureDerivation):
    def __init__(self, data_file, the_input_data=None):
        if not os.path.exists(data_file):
            raise Exception("No monthly energy production data found.")
        self.monthly_power_production = {}
        with open(data_file, newline="") as csvfile:
            next(csvfile)
            for row in csvfile:
                month, value = row.strip().split(";")
                self.monthly_power_production[month] = float(value)
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                "nominal_power": the_input_data["nominal_power"]
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "specific_yield": {}
        }

    def compute(self):
        def single_value_calc(power_yield):
            specific_yield = power_yield / self.input["nominal_power"].value
            return specific_yield

        self.output['specific_yield'] = {
            month: (power_yield, single_value_calc(power_yield))
            for month, power_yield in self.monthly_power_production.items()
        }


if __name__ == '__main__':
    the_target = MonthlySpecificYield(
        "monthly_power_production.csv",
        {
            "nominal_power": Measure("kW", 5),
        }
    )
    the_target.main()
    print(the_target.dump())
    # Dati di input
    months = the_target.monthly_power_production.keys()
    energy_produced = the_target.monthly_power_production.values()
    nominal_power = the_target.input["nominal_power"].value
    specific_yield = [energy / nominal_power for energy in energy_produced]
    print(f"{'Mese':<10}{'Energia Prodotta (kWh)':>25}{'Specific Yield (kWh/kW)':>30}")
    for month, energy, yield_ in zip(months, energy_produced, specific_yield):
        print(f"{month:<10}{energy:>25}{yield_:>30.2f}")
    plt.figure(figsize=(10, 6))
    plt.bar(months, specific_yield, color='skyblue')
    plt.xlabel('Mesi dell\'Anno')
    plt.ylabel('Specific Yield (kWh/kW)')
    plt.title('Specific Yield Mensile di un Impianto Fotovoltaico')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
