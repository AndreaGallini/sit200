# scheda 8.1 stima della riduzione delle emissioni 1005
from concept import Measure, MeasureDerivation


class EmissionReduction20Years(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {}
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'Tonnellate equivalenti di petrolio (TEP)': Measure("TEP", 25),
            'Riduzione di tonnellate di CO2': Measure("t", 50),
            'Rimboschimento equivalente': Measure("ettari/anno", 1.25)
        }

    def validate(self):
        # verificare unità di misura
        return True

    def compute(self):
        pass


if __name__ == '__main__':
    the_target = EmissionReduction20Years({})
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
