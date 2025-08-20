import utils


class MaxPhotovoltaicParallelPanelsNo:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.inverter_max_dc_input_current = 33.0  # A
        self.panel_max_dc_mpp = 11.25  # A
        self.max_parallel_panels_no = 0

    def compute(self):
        self.max_parallel_panels_no = self.inverter_max_dc_input_current // self.panel_max_dc_mpp

    def validate(self):
        # expected: inverter max dc input current (A) and panel max dc input current (A)
        if type(self.input_data) != list:
            print('Input data must be a list')
            return False
        if len(self.input_data) != 2:
            print("expecting 2 parameters, both expressed in A")
            return False
        if type(self.input_data[0]) != float or type(self.input_data[1]) != float:
            print("expecting float parameters, both expressed in A")
            return False
        return True

    def main(self, the_input_data=None, the_input_csv=None, the_output_csv=None):
        if the_input_data:
            self.input_data = the_input_data
            if self.validate():
                self.compute()
                return [self.max_parallel_panels_no]
            else:
                print('Input data not valid')
        elif the_input_csv and the_input_csv:
            self.input_data = csvinout.read_csv_data(the_input_csv)
            if self.validate():
                self.compute()
                csvinout.write_csv_data(the_output_csv, [self.max_parallel_panels_no])
                return None
            else:
                print("input data not valid")
                return None
        else:
            self.compute()
            print(
                f"inverter_max_dc_input_current {self.inverter_max_dc_input_current}\n"
                f"panel_max_dc_mpp {self.panel_max_dc_mpp}\n"
                f"max_parallel_panels_no {self.max_parallel_panels_no}"
            )


if __name__ == '__main__':
    the_target = MaxPhotovoltaicParallelPanelsNo()
    the_target.main()
