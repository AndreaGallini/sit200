# scheda 6.6 modello F8 definizione dei limiti delle classi di classificazione di producibilità mensile
from concept import Measure, MeasureDerivation

class MonthlyEnergyYieldClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_energy_yield': the_input_data['monthly_energy_yield'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.thresholds = {
            # TODO: correggere le classi
                "Molto bassa": 60,
                "Bassa": 100,
                "Media": 140,
                "Alta": 180,
                "Molto Alta": float('inf')
            }
        self.output = {
            "monthly_net_energy_class_thresholds": self.thresholds,
            "monthly_energy_yield_classes": {}
        }

    def validate(self):
        # verificare unità di misura e numerosità
        return True

    def compute(self):
        monthly_energy_yields = self.input["monthly_energy_yield"]
        for month, measure in monthly_energy_yields.items():
            monthly_energy_yield = measure.value
            for threshold_label, threshold_value in self.thresholds.items():
                if monthly_energy_yield < threshold_value:
                    self.output['monthly_energy_yield_classes'][month] = (monthly_energy_yield, threshold_label)
                    break


if __name__ == '__main__':
    the_target = MonthlyEnergyYieldClassification({
        'monthly_energy_yield': {
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
        }
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
