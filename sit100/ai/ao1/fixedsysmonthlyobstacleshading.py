# arancione ITE 9d ombreggiamento ostacoli
from .concept import Measure, MeasureDerivation, months
from .utils import log


class FixedSysMonthlyObstacleShading(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        if the_input_data is None:
            the_input_data = { "shading_obstacle": Measure("%", 0.0)}
        else:
            try:
                self.input = {
                    "shading_obstacle": the_input_data["shading_obstacle"]
                    }
            except KeyError:
                log("ERROR", "FixedSysMonthlyObstacleShading: missing input data")
        self.output = {
            "fixed_sys_monthly_obstacle_shading": {month: Measure("%", 0.0) for month in months}
        }

    def validate(self):
        if "shading_obstacle" not in self.input:
            log("ERROR", "FixedSysMonthlyObstacleShading: 'shading_obstacle' key missing in input data")
            return False

        shading_obstacle = self.input["shading_obstacle"]
        if not isinstance(shading_obstacle, Measure):
            log("ERROR", f"FixedSysMonthlyObstacleShading: data is not a Measure")
            return False
        if not (0 <= shading_obstacle.value <= 25):
            log("ERROR", f"FixedSysMonthlyObstacleShading: value is out of range (0-25)")
            return False
        return True

    def compute(self):
        for month in months:
            self.output["fixed_sys_monthly_obstacle_shading"][month] = self.input["shading_obstacle"]


if __name__ == '__main__':
    the_target = FixedSysMonthlyObstacleShading({"shading_obstacle": Measure("%", 2.3)})
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
