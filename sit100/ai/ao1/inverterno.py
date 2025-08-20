import utils


class InverterNo:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.panels_no = 125000
        self.parallel_panels_no = 2
        self.panel_string_length = 25
        self.inverter_no = 1250

    def compute(self):
        self.inverter_no = - (-self.panels_no//(self.parallel_panels_no*self.panel_string_length))

    def validate(self):
        # expected: number of panels, number of parallel panels, panel string length
        if type(self.input_data) != list:
            print('Input data must be a list')
            return False
        if len(self.input_data) != 3:
            print("expecting 2 parameters, both expressed in A")
            return False
        if type(self.input_data[0]) != int or type(self.input_data[1]) != int or type(self.input_data[2]) != int:
            print("expecting int parameters")
            return False
        return True

    def main(self, the_input_data=None, the_input_csv=None, the_output_csv=None):
        if the_input_data:
            self.input_data = the_input_data
            if self.validate():
                self.compute()
                return [self.inverter_no]
            else:
                print('Input data not valid')
        elif the_input_csv and the_input_csv:
            self.input_data = csvinout.read_csv_data(the_input_csv)
            if self.validate():
                self.compute()
                csvinout.write_csv_data(the_output_csv, [self.inverter_no])
                return None
            else:
                print("input data not valid")
                return None
        else:
            self.compute()
            print(
                f"number of panels {self.panels_no}\n"
                f"number of parallel panels {self.parallel_panels_no}\n"
                f"panel string length {self.panel_string_length}\n"
                f"inverter number {self.inverter_no}"
            )


if __name__ == '__main__':
    the_target = InverterNo()
    the_target.main()
