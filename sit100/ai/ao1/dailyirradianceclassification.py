# bistro modello C5 definizione dei limiti delle classi di classificazione irradiazione solari giornaliera media mensile
# sul piano dei moduli
from concept import Measure, MeasureDerivation


class DailyIrradiationClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "daily_irradiation_classes_thresholds": {
                "Molto bassa": 3.5,
                "Bassa": 4.5,
                "Media": 6.0,
                "Alta": 7.5,
                "Molto Alta": float('inf')
            },
            "daily_irradiation_classification": {
                'Gennaio': (1.7934049974072641, 'Molto Bassa'),
                'Febbraio': (2.641046009174657, 'Molto Bassa'),
                'Marzo': (3.7934446046898653, 'Bassa'),
                'Aprile': (4.452036339306356, 'Bassa'),
                'Maggio': (5.713566843464206, 'Media'),
                'Giugno': (5.8361713319226896, 'Media'),
                'Luglio': (6.441188107815142, 'Alta'),
                'Agosto': (6.1306821528704845, 'Alta'),
                'Settembre': (4.319930167956351, 'Bassa'),
                'Ottobre': (3.0540156209245812, 'Molto Bassa'),
                'Novembre': (2.1249371196155913, 'Molto Bassa'),
                'Dicembre': (1.3788739950698314, 'Molto Bassa')
            }
        }

    def validate(self):
        return True

    def compute(self):
        pass


if __name__ == '__main__':
    the_target = DailyIrradiationClassification({})
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
