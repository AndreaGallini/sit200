# O2 total area

import utils


class TotalArea:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.number_of_modules = 12500
        self.module_area = 2  # m2
        self.total_area = 25000  # m2

    def compute(self):
        self.total_area = self.number_of_modules * self.module_area

    def validate(self):
        data_schema = [
            int,
            int
        ]
        return tools.validate(self.input_data, data_schema)

    def main(self, the_input_data=None, the_input_csv=None, the_output_csv=None):
        if the_input_data:
            self.input_data = the_input_data
            if self.validate():
                self.compute()
                return [self.number_of_modules, self.module_area, self.total_area]
            else:
                print('Input data not valid')
                return None
        elif the_input_csv and the_input_csv:
            self.input_data = tools.read_csv_data(the_input_csv)
            if self.validate():
                self.compute()
                tools.write_csv_data(the_output_csv, [self.number_of_modules, self.module_area, self.total_area])
                return None
            else:
                print("input data not valid")
                return None
        else:
            self.compute()
            print(
                f"system power: {self.number_of_modules}\n"
                f"module area: {self.module_area}\n"
                f"total area: {self.total_area}"
            )


if __name__ == '__main__':
    the_target = TotalArea()
    the_target.main()
