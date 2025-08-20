# scheda 6.2 energia utile mensile 0812 modello D6
from concept import Measure, MeasureDerivation


class MonthlyNetEnergyClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_net_energy': the_input_data['monthly_net_energy'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.thresholds = {
                "Molto bassa": 60,
                "Bassa": 100,
                "Media": 140,
                "Alta": 180,
                "Molto Alta": float('inf')
            }
        self.output = {
            "monthly_net_energy_class_thresholds": self.thresholds,
            "monthly_net_energy_classes": {}
        }

    def validate(self):
        # verificare unità di misura e numerosità
        return True

    def compute(self):
        monthly_net_energy = self.input["monthly_net_energy"]
        monthly_net_energy_classes = {}
        for month, measure in monthly_net_energy.items():
            monthly_net_energy = measure.value
            for threshold_label, threshold_value in self.thresholds.items():
                if monthly_net_energy < threshold_value:
                    self.output['monthly_net_energy_classes'][month] = (monthly_net_energy, threshold_label)
                    break


if __name__ == '__main__':
    the_target = MonthlyNetEnergyClassification({
        'monthly_net_energy': {
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
