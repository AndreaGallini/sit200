# Arcobaleno 5 / scheda 6.10 classificazione dell'efficienza percentuale del sistema fotovoltaico
from .concept import Measure, MeasureDerivation


class SystemEfficiencyClassification(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'system_efficiency': the_input_data['system_efficiency'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.thresholds = {
                "Molto bassa": (65, "Generalmente gli impianti tipici di questa classe presentano una notevole "
                                    "quantità di perdite. Questa bassa efficienza può essere dovuta a una serie di "
                                    "problemi come un alto grado di ombreggiamento, un'inclinazione subottimale dei "
                                    "pannelli, moduli fotovoltaici di qualità scadente, o inverter inefficaci. Anche "
                                    "temperature elevate senza adeguata ventilazione possono ridurre sensibilmente le "
                                    "prestazioni."),
                "Bassa": (70, "In questa fascia, l'efficienza è ancora inferiore rispetto alle medie del settore, "
                              "suggerendo un'installazione con condizioni non ottimali o componenti di media qualità."),
                "Media": (75, "Un impianto con efficienza media presenta una discreta capacità di conversione, con "
                              "perdite contenute grazie a un’installazione ragionevolmente ottimizzata e a componenti "
                              "standard. Le perdite, in questo caso, sono prevalentemente legate a fattori comuni, "
                              "come un certo grado di ombreggiamento o temperature elevate che impattano l'efficienza "
                              "dei moduli."),
                "Alta": (80, "Un’efficienza alta denota un sistema fotovoltaico ben progettato, con perdite ridotte al "
                             "minimo. Gli impianti in questa fascia generalmente sfruttano orientamento e inclinazione "
                             "ottimali, pannelli di alta qualità e inverter efficienti, oltre a una gestione delle "
                             "ombre ottimizzata e una buona ventilazione."),
                "Molto Alta": (float('inf'), "Questa classe rappresenta l’eccellenza nell'efficienza di conversione "
                                             "fotovoltaica, con perdite minime. Gli impianti in questa categoria "
                                             "sfruttano i migliori materiali e tecnologie, con un'installazione "
                                             "perfettamente ottimizzata per irraggiamento e inclinazione, un "
                                             "eccellente sistema di gestione dell'ombreggiamento e soluzioni per "
                                             "ridurre le perdite termiche e di conversione al minimo.")
            }
        self.output = {
            "system_efficiency_value": 0.0,
            "system_efficiency_energy_class": "",
            "system_efficiency_energy_comment": ""
        }

    def validate(self):
        # verificare unità di misura
        return True

    def compute(self):
        system_efficiency = self.input["system_efficiency"].value
        self.output["system_efficiency_value"] = system_efficiency
        for threshold_label, (threshold_value, threshold_comment) in self.thresholds.items():
            if system_efficiency < threshold_value:
                self.output['system_efficiency_energy_class'] = threshold_label
                self.output['system_efficiency_energy_comment'] = threshold_comment
                break


if __name__ == '__main__':
    the_target = SystemEfficiencyClassification({
        'system_efficiency': Measure("%", 48)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
