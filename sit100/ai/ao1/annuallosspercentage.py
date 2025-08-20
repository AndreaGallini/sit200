# arancione EE 11 perdita annua percentuale del generatore fotovoltaico
from .concept import Measure, MeasureDerivation


class AnnualLossPercentage(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "theoretical_annual_yield": the_input_data["theoretical_annual_yield"],
                "annual_energy_yield": the_input_data["annual_energy_yield"]
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "annual_loss_percentage": Measure("%", 0.0)
        }

    def validate(self):
        for key, value in self.input.items():
            if not isinstance(value, Measure):
                print(f"Invalid measure value for {key}: not a Measure")
                return False
            if value.unit != "kWh/kWp":
                print(f"Invalid measure value for {key}")
                return False
        return True

    def compute(self):
        theoretical_annual_yield = self.input["theoretical_annual_yield"].value
        annual_energy_yield = self.input["annual_energy_yield"].value
        annual_loss_percentage = round(100.0 - annual_energy_yield / theoretical_annual_yield * 100.0, 2)
        self.output["annual_loss_percentage"] = Measure("%", annual_loss_percentage)


if __name__ == '__main__':
    the_target = AnnualLossPercentage({
        "annual_energy_yield": Measure("kWh/kWp", 1200.0),
        "theoretical_annual_yield": Measure("kWh/kWp", 1500.0),
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
