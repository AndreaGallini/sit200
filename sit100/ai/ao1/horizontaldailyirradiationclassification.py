# bistro modello B4 definizione dei limiti delle classi di classificazione irradiazione solari giornaliera media mensile
# su un piano orizzontale
from concept import Measure, MeasureDerivation


class HorizontalDailyIrradiationClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "horizontal_daily_irradiation_classes_thresholds": {
                "Molto bassa": 2.0,
                "Bassa": 3.5,
                "Media": 5.0,
                "Alta": 6.5,
                "Molto Alta": float('inf')
            },
            "horizontal_daily_irradiation_classification": {
                'Gennaio': (1.78, 'Molto Bassa'),
                'Febbraio': (2.57, 'Bassa'),
                'Marzo': (3.71, 'Media'),
                'Aprile': (4.9, 'Media'),
                'Maggio': (5.95, 'Alta'),
                'Giugno': (6.47, 'Alta'),
                'Luglio': (6.47, 'Alta'),
                'Agosto': (5.68, 'Alta'),
                'Settembre': (4.53, 'Media'),
                'Ottobre': (3.24, 'Bassa'),
                'Novembre': (2.05, 'Bassa'),
                'Dicembre': (1.48, 'Molto Bassa')}
        }

    def validate(self):
        return True

    def compute(self):
        pass


if __name__ == '__main__':
    the_target = HorizontalDailyIrradiationClassification({})
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
