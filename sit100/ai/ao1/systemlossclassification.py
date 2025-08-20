# scheda 5.3 perdite di sistema 0801
from concept import Measure, MeasureDerivation


class SystemLossClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'system_loss': the_input_data['system_loss'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.thresholds = {
                "Molto bassa": 10,
                "Bassa": 15,
                "Media": 20,
                "Alta": 25,
                "Molto Alta": float('inf')
            }
        self.output = {
            "system_loss_classes_thresholds": self.thresholds,
            "system_loss_class": "Media"
        }

    def validate(self):
        # verificare unità di misura
        return True

    def compute(self):
        system_loss = self.input["system_loss"].value
        for threshold_label, threshold_value in self.thresholds.items():
            if system_loss < threshold_value:
                self.output['system_loss_class'] = threshold_label
                break


if __name__ == '__main__':
    the_target = SystemLossClassification({
        'system_loss': Measure("%", 15.3)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
