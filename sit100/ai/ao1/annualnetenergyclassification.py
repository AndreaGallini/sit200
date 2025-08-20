# scheda 6.4 modello E7 limiti delle classi di classificazione di energia utile annua
from .concept import Measure, MeasureDerivation


class AnnualNetEnergyClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_net_energy': the_input_data['annual_net_energy'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.thresholds = {
                "Molto bassa": (900,"L’area presenta una bassissima irradiazione, poco favorevole per impianti "
                                "fotovoltaici."),
                "Bassa": (1100, "Irradianza risulta modesta e la conseguente resa energetica limitata; adatta solo per "
                                "progetti locali e ben ottimizzati."),
                "Media": (1300, "Il sito di installazione presenta un contesto di condizioni energetiche moderate, "
                                "la fattibilità economica può essere accettabile per progetti residenziali e "
                                "commerciali."),
                "Alta": (1500, "Buona irradiazione, alta efficienza e resa economica interessante per gli impianti "
                               "fotovoltaici anche di medie e grandi dimensioni."),
                "Molto Alta": (float('inf'), "Questo indica che la località ha un'ottima esposizione solare e "
                                             "condizioni favorevoli per la produzione di energia solare. Un impianto "
                                             "fotovoltaico in questa area sarebbe in grado di produrre una quantità "
                                             "significativa di energia elettrica, rendendo l'investimento molto "
                                             "conveniente. ")
            }
        self.output = {
            "annual_net_energy_value": 0.0,
            "annual_net_energy_class": "",
            "annual_net_energy_comment": "",
        }

    def validate(self):
        # verificare unità di misura
        return True

    def compute(self):
        annual_net_energy = self.input["annual_net_energy"].value
        self.output["annual_net_energy_value"] = annual_net_energy
        for threshold_label, (threshold_value, threshold_comment) in self.thresholds.items():
            if annual_net_energy < threshold_value:
                self.output['annual_net_energy_class'] = threshold_label
                self.output['annual_net_energy_comment'] = threshold_comment
                break


if __name__ == '__main__':
    the_target = AnnualNetEnergyClassification({
        'annual_net_energy': Measure("kWh/m2/anno", 1650)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
