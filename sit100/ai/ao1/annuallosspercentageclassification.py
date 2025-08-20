# scheda 6.9 energia elettrica annua teoricamente ottenibile
from .concept import Measure, MeasureDerivation


class AnnualLossPercentageClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'annual_loss_percentage': the_input_data['annual_loss_percentage'],
            }
        except KeyError:
            print("missing input value")
            quit()

        self.thresholds = {
                "Molto bassa": (10, "In questo caso le perdite di sistema molto basse rappresentano una condizione "
                                "ideale e sono indice di un impianto altamente ottimizzato."),
                "Bassa": (15, "Le perdite di sistema in questa classe sono lievemente superiori rispetto alla classe "
                          "-Molto Bassa-, ma sono comunque indicative di un impianto ben progettato composto da "
                              "attrezzature di qualità."),
                "Media": (20, "Una classe di perdite medie indica che l’impianto è soggetto a inefficienze moderate "
                          "che, sebbene non compromettano gravemente le performance complessive, segnalano possibili "
                          "margini di miglioramento."),
                "Alta": (25, "Questa classe indica perdite di sistema rilevanti che compromettono significativamente "
                         "le prestazioni dell’impianto fotovoltaico."),
                "Molto Alta": (float('inf'), "Le perdite molto alte indicano una situazione critica in cui l’impianto "
                               "ha prestazioni gravemente compromesse. In questa classe, oltre il 25% dell’energia "
                               "teorica viene dispersa o non convertita sufficientemente.")
            }
        self.output = {
            "annual_loss_percentage_value": 0.0,
            "annual_loss_percentage_class": "",
            "annual_loss_percentage_comment": ""
        }

    def validate(self):
        # verificare unità di misura
        return True

    def compute(self):
        annual_loss_percentage = self.input["annual_loss_percentage"].value
        self.output["annual_loss_percentage_value"] = annual_loss_percentage
        for threshold_label, (threshold_value, threshold_comment) in self.thresholds.items():
            if annual_loss_percentage < threshold_value:
                self.output['annual_loss_percentage_class'] = threshold_label
                self.output['annual_loss_percentage_comment'] = threshold_comment
                break


if __name__ == '__main__':
    the_target = AnnualLossPercentageClassification({
        'annual_loss_percentage': Measure("kWh/m2/anno", 18)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
