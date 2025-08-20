# arancione EE 4 producibilità mensile
from .concept import Measure, MeasureDerivation, months


class MonthlyEnergyYield(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_net_energy': the_input_data['monthly_net_energy'],
                'monthly_efficiency_percentage': the_input_data['monthly_efficiency_percentage']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "monthly_energy_yield": {month: Measure("kWh/kWp", 0.0) for month in months}
        }

    def validate(self):
        # 12 mesi sia per l'energia utile sia per l'efficienza
        # controllare unità di misura
        return True

    def compute(self):
        monthly_net_energy = self.input['monthly_net_energy']
        monthly_efficiency_percentage = self.input['monthly_efficiency_percentage']
        monthly_energy_yield = {}
        for month in monthly_net_energy:
            energy = monthly_net_energy[month].value
            efficiency_percentage = monthly_efficiency_percentage[month].value / 100
            energy_yield = energy * efficiency_percentage
            monthly_energy_yield[month] = Measure("kWh/kWp", round(energy_yield, 2))
        self.output["monthly_energy_yield"] = monthly_energy_yield


if __name__ == '__main__':
    the_target = MonthlyEnergyYield({
        'monthly_net_energy': {
            "GEN": Measure("kWh/m2/mese", 85.0),
            "FEB": Measure("kWh/m2/mese", 95.0),
            "MAR": Measure("kWh/m2/mese", 110.0),
            "APR": Measure("kWh/m2/mese", 120.0),
            "MAG": Measure("kWh/m2/mese", 125.0),
            "GIU": Measure("kWh/m2/mese", 115.0),
            "LUG": Measure("kWh/m2/mese", 110.0),
            "AGO": Measure("kWh/m2/mese", 100.0),
            "SET": Measure("kWh/m2/mese", 95.0),
            "OTT": Measure("kWh/m2/mese", 80.0),
            "NOV": Measure("kWh/m2/mese", 70.0),
            "DIC": Measure("kWh/m2/mese", 75.0),
        },
        'monthly_efficiency_percentage': {
            "GEN": Measure("%", 64.65),
            "FEB": Measure("%", 85.91),
            "MAR": Measure("%", 105.12),
            "APR": Measure("%", 105.06),
            "MAG": Measure("%", 118.20),
            "GIU": Measure("%", 133.69),
            "LUG": Measure("%", 153.35),
            "AGO": Measure("%", 145.31),
            "SET": Measure("%", 123.68),
            "OTT": Measure("%", 116.00),
            "NOV": Measure("%", 82.56),
            "DIC": Measure("%", 69.99)
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
