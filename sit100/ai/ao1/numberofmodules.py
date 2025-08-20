# O1 Number of Modules

import utils


class NumberOfModules:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.module_power = 400  # W
        self.system_power = 5  # MW
        self.number_of_modules = 0

    def compute(self):
        self.number_of_modules = self.system_power * 1000000 // self.module_power

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
                return [self.module_power, self.system_power, self.number_of_modules]
            else:
                print('Input data not valid')
                return None
        elif the_input_csv and the_input_csv:
            self.input_data = tools.read_csv_data(the_input_csv)
            if self.validate():
                self.compute()
                tools.write_csv_data(the_output_csv, [self.module_power, self.system_power, self.number_of_modules])
                return None
            else:
                print("input data not valid")
                return None
        else:
            self.compute()
            print(
                f"system power: {self.system_power}\n"
                f"module power: {self.module_power}\n"
                f"number of modules: {self.number_of_modules}\n"
            )


if __name__ == '__main__':
    the_target = NumberOfModules()
    the_target.main()
