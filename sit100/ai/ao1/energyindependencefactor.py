# RED E9E Energy Independence Factor
from concept import Measure, MeasureDerivation
import utils

class EnergyIndependenceFactor(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                "self_consumed_energy": the_input_data["self_consumed_energy"],
                "total_energy_consumed": the_input_data["total_energy_consumed"]
            }
        except KeyError:
            print("incorrect input value")
            quit()
        self.output = {
            "energy_independence_factor": Measure("%", 0.0),
            "energy_independence_factor_level": "",
        }

    def compute(self):
        def energy_independence_factor_level(energy_independence_factor_value):
            bands = ["molto basso", "basso", "moderato", "alto", "molto alto"]
            band_number = len(bands)
            band_size = 1 / band_number
            for x in range(band_number):
                threshold = x * band_size
                if threshold < energy_independence_factor_value < threshold + band_size:
                    return bands[x]
        self_consumed_energy = self.input["self_consumed_energy"].value
        total_energy_consumed = self.input["total_energy_consumed"].value
        energy_independence_factor = self_consumed_energy / total_energy_consumed
        self.output['energy_independence_factor'] = (
            Measure("%", tools.proper_round(energy_independence_factor * 100, 1))
        )
        self.output['energy_independence_factor_level'] = (
            energy_independence_factor_level(energy_independence_factor)
        )


if __name__ == '__main__':
    the_target = EnergyIndependenceFactor(
        {
            "self_consumed_energy": Measure("kW", 1500.0),
            "total_energy_consumed": Measure("kW", 1800.0)
        }
    )
    the_target.main()
    print(the_target.dump())
