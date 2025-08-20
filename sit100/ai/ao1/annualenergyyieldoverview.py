# scheda 6.16 bistro H10 modello di sintesi dei risultati di producibilità annua
from concept import Measure, MeasureDerivation


class AnnualEnergyYieldOverview(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_net_energy': the_input_data['annual_net_energy'],
                'annual_nominal_energy_yield': the_input_data['annual_nominal_energy_yield'],
                'annual_nominal_energy': the_input_data['annual_nominal_energy'],
                'system_efficiency': the_input_data['system_efficiency'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.labels = {
            "annual_net_energy": "Energia utile annua",
            "annual_nominal_energy_yield": "Producibilità annua teorica",
            "annual_nominal_energy": "Energia elettrica teoricamente ottenibile",
            "system_efficiency": "Efficienza percentuale del sistema"
        }
        self.output = {
            'overview': ""
        }

    def validate(self):
        # verificare unità di misura
        return True

    def compute(self):
        msg = ""
        for key, measure in self.input.items():
            value = measure.value
            msg += key + ": " + str(value) + "\n"
        self.output['overview'] = msg


if __name__ == '__main__':
    the_target = AnnualEnergyYieldOverview({
        'annual_net_energy': Measure("kWh/m2/anno", 1650),
        "annual_nominal_energy_yield":  Measure("kWh/kWp", 1440),
        "annual_nominal_energy": Measure("kWh/anno", 29376),
        "system_efficiency": Measure("%", 80)
    })
    if the_target.validate():
        the_target.main()
        msg = the_target.output['overview']
        print(msg)
    else:
        print("input not valid, error")
        print(the_target.output)
