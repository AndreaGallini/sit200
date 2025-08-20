# scheda 6.13 classificazione dell'efficienza percentuale del sistema fotovoltaico
from .concept import Measure, MeasureDerivation


class MonthlySystemEfficiencyClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'monthly_system_efficiency': the_input_data['monthly_system_efficiency'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.thresholds = {
                "Molto bassa": 65,
                "Bassa": 70,
                "Media": 75,
                "Alta": 80,
                "Molto Alta": float('inf')
            }
        self.output = {
            "monthly_system_efficiency_classes_thresholds": self.thresholds,
            "monthly_system_efficiency_classes": {}
        }

    def validate(self):
        # verificare unità di misura e numerosità
        return True

    def compute(self):
        monthly_system_efficiency = self.input["monthly_system_efficiency"]
        for month, measure in monthly_system_efficiency.items():
            the_monthly_system_efficiency = measure.value
            for threshold_label, threshold_value in self.thresholds.items():
                if the_monthly_system_efficiency < threshold_value:
                    self.output['monthly_system_efficiency_classes'][month] = \
                        (the_monthly_system_efficiency, threshold_label)
                    break


if __name__ == '__main__':
    the_target = MonthlySystemEfficiencyClassification({
        'monthly_system_efficiency': {
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
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
