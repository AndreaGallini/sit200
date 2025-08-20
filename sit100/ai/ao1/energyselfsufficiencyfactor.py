# RED E10E Energy Self-Sufficiency Factor
from concept import Measure, MeasureDerivation
import utils


class EnergySelfSufficiencyFactor(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                "energy_yield": the_input_data["energy_yield"],
                "total_energy_consumed": the_input_data["total_energy_consumed"]
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "energy_self_sufficiency_factor": Measure("%", 0.0),
            "energy_self_sufficiency_factor_level": "",
        }

    def compute(self):
        def energy_self_sufficiency_factor_level(energy_self_sufficiency_factor_value):
            bands = ["molto basso", "basso", "moderato", "alto", "molto alto"]
            band_number = len(bands)
            band_size = 1 / band_number
            for x in range(band_number):
                threshold = x * band_size
                if threshold < energy_self_sufficiency_factor_value < threshold + band_size:
                    return bands[x]

        energy_yield = self.input["energy_yield"].value
        total_energy_consumed = self.input["total_energy_consumed"].value
        energy_self_sufficiency_factor = energy_yield / total_energy_consumed
        self.output['energy_independence_factor'] = (
            Measure("%", tools.proper_round(energy_self_sufficiency_factor * 100, 1))
        )
        self.output['energy_independence_factor_level'] = (
            energy_self_sufficiency_factor_level(energy_self_sufficiency_factor)
        )


if __name__ == '__main__':
    the_target = EnergySelfSufficiencyFactor(
        {
            "energy_yield": Measure("kW", 1400.0),
            "total_energy_consumed": Measure("kW", 1800.0)
        }
    )
    the_target.main()
    print(the_target.dump())
