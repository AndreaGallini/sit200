from concept import MeasureDerivation
#  Model A1
import math
import weighting
from concept import Measure, MeasureDerivation
import utils
import matplotlib.pyplot as plt


class IdaSuitabilityAssessment(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                "values": the_input_data["values"],
                "weights": the_input_data["weights"]
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            "ida": 0.0,
            'suitability_label': '',
            'suitability_description': ''
        }

    def compute(self):
        values = self.input["values"]
        weights = self.input["weights"]
        ida = weighting.Weighting(values=values, weights=weights)
        ida_index = ida.get_index()
        self.output["ida"] = ida_index
        classes = [
            {'threshold': 20, 'label': 'Esclusione', 'description': "L'area è totalmente inadatta per l'impianto. Non "
                                                                    "soddisfa i requisiti minimi necessari"},
            {'threshold': 40, 'label': 'Scarsa idoneità', 'description': "L'area presenta significative carenze in "
                                                                         "termini di idoneità. Potrebbe necessitare di "
                                                                         "modifiche sostanziali per essere considerata."},
            {'threshold': 60, 'label': 'Moderata idoneità', 'description': "L'area ha una idoneità moderata. Potrebbe "
                                                                           "essere adatta con alcuni aggiustamenti e "
                                                                           "investimenti."},
            {'threshold': 80, 'label': 'Buona idoneità', 'description': "L'area è per lo più idonea per l'impianto con "
                                                                        "pochi miglioramenti richiesti."},
            {'threshold': 100, 'label': 'Eccellente idoneità', 'description': "L'area è perfettamente idonea e conforme"
                                                                              "per l'impianto."},
        ]
        thresholds = [c['threshold'] for c in classes]
        labels = [c['label'] for c in classes]
        descriptions = [c['description'] for c in classes]
        for i, threshold in enumerate(thresholds):
            if ida_index < threshold:
                self.output['suitability_label'] = labels[i]
                self.output['suitability_description'] = descriptions[i]
                break
        print("IDA:", self.output['ida'], self.output['suitability_label'])
        print(self.output['suitability_description'])

    def plot(self):
        ida = self.output["ida"]
        ida_label = str(ida)
        ida_angle = (1 - ida / 100) * math.pi
        colors = ["#00DD00", "#d6ff00", "#ffff00", "#ffc100", '#ff0000']
        values = [100, 80, 60, 40, 20, 0]
        fig = plt.figure(figsize=(18, 18))
        ax = fig.add_subplot(projection="polar")
        ax.bar(x=[0.0, 0.63, 1.26, 1.89, 2.51], width=0.63, height=0.5, bottom=2,
               linewidth=3, edgecolor="white",
               color=colors, align="edge")
        for loc, val in zip([0.0, 0.63, 1.26, 1.89, 2.51, 3.14], values):
            plt.annotate(val, xy=(loc, 2.5), ha="right" if val <= 20 else "left", fontsize=20)
        plt.annotate(ida_label, xytext=(0, 0), xy=(ida_angle, 2.0),
                     arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="black", shrinkA=0),
                     bbox=dict(boxstyle="circle", facecolor="black", linewidth=2.0, ),
                     fontsize=45, color="white", ha="center"
                     )
        plt.title("IDA " + ida_label, loc="center", pad=20, fontsize=35, fontweight="bold")
        ax.set_axis_off()
        plt.show()


if __name__ == '__main__':
    the_target = IdaSuitabilityAssessment({"values": [7, 1, 4], "weights": [2, 5, 2]})
    the_target.compute()
    the_target.plot()
    the_target.dump()
