import utils


class FinalPanelsPowerArea:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.inverter_no = 1500
        self.parallel_panels_no = 2
        self.panel_string_length = 25
        self.panel_nominal_power = 40  # W
        self.panel_area = 0.8  # m2
        self.panel_no = None  # number (example 120000)
        self.installed_power = None  # MW (example 1.5)
        self.system_area = None  # km2 (example 3)

    def compute(self):
        self.panel_no = self.inverter_no*self.parallel_panels_no*self.panel_string_length
        self.installed_power = self.panel_no*self.panel_nominal_power
        self.system_area = self.panel_no*self.panel_area

    def validate(self):
        data_schema = [
            int,    # 0- number of inverter
            int,    # 1- number of parallel panels
            int,    # 2- panel string length
            float,  # 3- panel nominal power
            float   # 4- panel area
        ]
        return csvinout.validate(self.input_data, data_schema)

    def main(self, the_input_data=None, the_input_csv=None, the_output_csv=None):
        if the_input_data:
            self.input_data = the_input_data
            if self.validate():
                self.compute()
                return [self.panel_no, self.installed_power, self.system_area]
            else:
                print('Input data not valid')
                return None
        elif the_input_csv and the_input_csv:
            self.input_data = csvinout.read_csv_data(the_input_csv)
            if self.validate():
                self.compute()
                csvinout.write_csv_data(the_output_csv, [self.panel_no, self.installed_power, self.system_area])
                return None
            else:
                print("input data not valid")
                return None
        else:
            self.compute()
            print(
                f"inverter number: {self.inverter_no}\n"
                f"parallel panel number: {self.parallel_panels_no}\n"
                f"panel string: {self.panel_string_length}\n"
                f"panel area: {self.panel_area}\n"
                f"panel nominal power: {self.panel_nominal_power}\n"
                f"panels number: {self.panel_no}\n"
                f"installed power: {self.installed_power}\n"
                f"system area: {self.system_area}\n"
            )


if __name__ == '__main__':
    the_target = FinalPanelsPowerArea()
    the_target.main()
