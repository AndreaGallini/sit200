# scheda 6.9 energia elettrica annua teoricamente ottenibile
from concept import Measure, MeasureDerivation

class AnnualNominalEnergyClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_nominal_energy': the_input_data['annual_nominal_energy'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.thresholds = {
                "Molto bassa": 10000,
                "Bassa": 12000,
                "Media": 14000,
                "Alta": 16000,
                "Molto Alta": float('inf')
            }
        self.output = {
            "annual_nominal_energy_classes_thresholds": self.thresholds,
            "annual_nominal_energy_class": "Molto Alta"
        }

    def validate(self):
        # verificare unità di misura
        return True

    def compute(self):
        annual_net_energy = self.input["annual_nominal_energy"].value
        for threshold_label, threshold_value in self.thresholds.items():
            if annual_net_energy < threshold_value:
                self.output['annual_nominal_energy_class'] = threshold_label
                break


if __name__ == '__main__':
    the_target = AnnualNominalEnergyClassification({
        'annual_nominal_energy': Measure("kWh/m2/anno", 17000)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
