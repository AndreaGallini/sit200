# Arancione SOLE 9 producibilità annua teorica
# input: radiazione solare annua
import json
from .concept import Measure, MeasureDerivation, ClimatePosition, months


class TheoreticalAnnualYield(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_solar_radiation': the_input_data['annual_solar_radiation'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'theoretical_annual_yield': Measure("kWh/kWp", 0)
        }

    def validate(self):
        if self.input['annual_solar_radiation'] is None:
            return False
        if not isinstance(self.input['annual_solar_radiation'], Measure):
            return False
        return True

    def compute(self):
        annual_solar_radiation = self.input['annual_solar_radiation'].value
        self.output['theoretical_annual_yield'] = Measure("kWh/kWp", annual_solar_radiation)


if __name__ == '__main__':
    the_target = TheoreticalAnnualYield({
        "annual_solar_radiation": Measure("kWh/mq", 0.1),
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
