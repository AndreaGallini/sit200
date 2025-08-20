# scheda 6.17 bistro I11 modello di sintesi dei risultati di producibilità mensile
from concept import Measure, MeasureDerivation


class MonthlyEnergyYieldOverview(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_energy_yield': the_input_data['monthly_energy_yield'],
                'monthly_net_energy': the_input_data['monthly_net_energy'],
                'monthly_system_efficiency': the_input_data['monthly_system_efficiency'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.labels = {
            "monthly_energy_yield": "Producibilità mensile",
            'monthly_net_energy': "Valori di energia utile mensile",
            'monthly_system_efficiency': "Efficienza percentuale mensile",
        }
        self.output = {
            'overview': ""
        }

    def validate(self):
        # verificare unità di misura e lunghezza 12 mesi
        return True

    def compute(self):
        pass

    def dump(self):
        msg = ""
        for month, monthly_energy_yield in self.input['monthly_energy_yield'].items():
            the_monthly_energy_yield = monthly_energy_yield.dump()
            the_monthly_net_energy = self.input['monthly_net_energy'][month].dump()
            the_monthly_system_efficiency = self.input['monthly_system_efficiency'][month].dump()
            msg += f"{month} {the_monthly_energy_yield} {the_monthly_net_energy} {the_monthly_system_efficiency}\n"
        annual_energy_yield = sum([m.value for m in self.input['monthly_energy_yield'].values()])
        annual_net_energy = sum(m.value for m in self.input['monthly_net_energy'].values())
        annual_system_efficiency = sum(m.value for m in self.input['monthly_system_efficiency'].values())/12
        grand_totals = f"Annuo {annual_energy_yield} {annual_net_energy} {annual_system_efficiency:.2f}%\n"
        return msg + grand_totals


if __name__ == '__main__':
    the_target = MonthlyEnergyYieldOverview({
        'monthly_energy_yield': {
            "gennaio": Measure("kWh/kWp", 70.0),
            "febbraio": Measure("kWh/kWp", 85.0),
            "marzo": Measure("kWh/kWp", 120.0),
            "aprile": Measure("kWh/kWp", 140.0),
            "maggio": Measure("kWh/kWp", 160.0),
            "giugno": Measure("kWh/kWp", 170.0),
            "luglio": Measure("kWh/kWp", 165.0),
            "agosto": Measure("kWh/kWp", 150.0),
            "settembre": Measure("kWh/kWp", 130.0),
            "ottobre": Measure("kWh/kWp", 110.0),
            "novembre": Measure("kWh/kWp", 80.0),
            "dicembre": Measure("kWh/kWp", 60.0),
        },
        "monthly_net_energy":  {
            "gennaio": Measure("kWh/m2/mese", 80.0),
            "febbraio": Measure("kWh/m2/mese", 100.0),
            "marzo": Measure("kWh/m2/mese", 140.0),
            "aprile": Measure("kWh/m2/mese", 160.0),
            "maggio": Measure("kWh/m2/mese", 180.0),
            "giugno": Measure("kWh/m2/mese", 200.0),
            "luglio": Measure("kWh/m2/mese", 190.0),
            "agosto": Measure("kWh/m2/mese", 170.0),
            "settembre": Measure("kWh/m2/mese", 150.0),
            "ottobre": Measure("kWh/m2/mese", 120.0),
            "novembre": Measure("kWh/m2/mese", 90.0),
            "dicembre": Measure("kWh/m2/mese", 70.0),
        },
        "monthly_system_efficiency": {
            "gennaio": Measure("%", 64.0),
            "febbraio": Measure("%", 70.0),
            "marzo": Measure("%", 75.0),
            "aprile": Measure("%", 80.0),
            "maggio": Measure("%", 85.0),
            "giugno": Measure("%", 88.0),
            "luglio": Measure("%", 87.0),
            "agosto": Measure("%", 85.0),
            "settembre": Measure("%", 83.0),
            "ottobre": Measure("%", 78.0),
            "novembre": Measure("%", 70.0),
            "dicembre": Measure("%", 64.0),
        }
    })
    if the_target.validate():
        the_target.main()
        msg = the_target.dump()
        print(msg)
    else:
        print("input not valid, error")
        print(the_target.output)
