import csv
import os.path


class MaxPhotoVoltaicStringLength:
    def __init__(self):
        self.average_dc_input_voltage_per_mpp = 0.0  # V
        self.max_dc_input_voltage_per_mpp = 0.0  # V
        self.min_dc_input_voltage_per_mpp = 0.0  # V
        self.max_dc_input_voltage = 0.0  # V
        self.panel_max_voltage_per_mpp = 0.0  # V
        self.panel_max_voltage_open = 0.0  # V
        self.max_panel_string_length = 0

    def set_average_dc_input_voltage_per_mpp(self, the_average_dc_input_voltage_per_mpp):
        self.average_dc_input_voltage_per_mpp = the_average_dc_input_voltage_per_mpp

    def set_max_dc_input_voltage_per_mpp(self, the_max_dc_input_voltage_per_mpp):
        self.max_dc_input_voltage_per_mpp = the_max_dc_input_voltage_per_mpp

    def set_min_dc_input_voltage_per_mpp(self, the_min_dc_input_voltage_per_mpp):
        self.min_dc_input_voltage_per_mpp = the_min_dc_input_voltage_per_mpp

    def set_max_dc_input_voltage(self, the_max_dc_input_voltage):
        self.max_dc_input_voltage = the_max_dc_input_voltage

    def set_panel_max_voltage_per_mpp(self, the_panel_max_voltage_per_mpp):
        self.panel_max_voltage_per_mpp = the_panel_max_voltage_per_mpp

    def set_panel_max_voltage_open(self, the_panel_max_voltage_open):
        self.panel_max_voltage_open = the_panel_max_voltage_open

    def get_max_panel_string_length(self):
        self.compute_max_panel_string_length()
        return self.max_panel_string_length

    def main(self, csvfile_in=None, csvfile_name_out=None):
        # set exemplary data o get data from a csv file and compute result
        if csvfile_in is None and csvfile_name_out is None:
            self.set_average_dc_input_voltage_per_mpp(35)
            self.set_max_dc_input_voltage_per_mpp(480)
            self.set_min_dc_input_voltage_per_mpp(200)
            self.set_max_dc_input_voltage(600)
            self.set_panel_max_voltage_per_mpp(40)
            self.set_panel_max_voltage_open(48)
            self.compute_max_panel_string_length()
            self.output2display()
        elif os.path.isfile(csvfile_in):
            self.extract(csvfile_in)
            self.compute_max_panel_string_length()
            self.output2csv(csvfile_name_out)
        else:
            print('Please, input two valid csv files: the first one for input and the second one for output')
            print('The first one must exists. The second one, if exists, will be overwritten')

    def extract(self, the_csvfile_in):
        # extract data from csv file:
        # - average_dc_input_voltage_per_mpp
        # - max_dc_input_voltage_per_mpp
        # - min_dc_input_voltage_per_mpp
        # - max_dc_input_voltage
        # - panel_max_voltage_per_mpp
        # - panel_max_voltage_open
        with open(the_csvfile_in, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            try:
                row = next(reader)
                try:
                    self.set_average_dc_input_voltage_per_mpp(int(row[0]))
                    self.set_max_dc_input_voltage_per_mpp(int(row[1]))
                    self.set_min_dc_input_voltage_per_mpp(int(row[2]))
                    self.set_max_dc_input_voltage(int(row[3]))
                    self.set_panel_max_voltage_per_mpp(int(row[4]))
                    self.set_panel_max_voltage_open(int(row[5]))
                except ValueError as e:
                    print(f"Please input a valid csv file, containing only integer data. Error: {e}")
            except StopIteration:
                print(
                    'Please input a not empty csv file with 6 columns:\n'
                    '- average dc input voltage per MPP\n'
                    '- max dc input voltage per MPP\n'
                    '- min dc input voltage per MPP\n'
                    '- max dc input voltage\n'
                    '- panel: max voltage per MPP\n'
                    '- panel: max open circuit voltage\n'
                    )
                return None

    def output2display(self):
        # output computed result to console
        print(
            f"Average DC input voltage per MPP: {self.average_dc_input_voltage_per_mpp}\n"
            f"Max DC input voltage per MPP: {self.max_dc_input_voltage_per_mpp}\n"
            f"Min DC input voltage per MPP: {self.min_dc_input_voltage_per_mpp}\n"
            f"Max DC input voltage: {self.max_dc_input_voltage}\n"
            f"Panel max voltage per MPP: {self.panel_max_voltage_per_mpp}\n"
            f"Panel max open circuit voltage: {self.panel_max_voltage_open}\n"
            f"Max number of panels per string: {self.max_panel_string_length}\n"
        )

    def output2csv(self, csvfile_name_out):
        # output computed result to csv file
        csvfile = open(csvfile_name_out, 'w')
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow([self.max_panel_string_length])

    def compute_max_panel_string_length(self):
        the_average_dc_input_voltage_per_mpp = (self.max_dc_input_voltage_per_mpp+self.min_dc_input_voltage_per_mpp)/2
        the_max_panel_string_length = the_average_dc_input_voltage_per_mpp // self.panel_max_voltage_per_mpp
        indicator = the_max_panel_string_length * self.panel_max_voltage_open
        if indicator > self.max_dc_input_voltage:
            self.max_panel_string_length = the_max_panel_string_length-1
            self.compute_max_panel_string_length()
        else:
            self.max_panel_string_length = the_max_panel_string_length
        print(
            f"(Max no. of panels: {self.max_panel_string_length}, "
            f"average DC input voltage per MPP: {the_average_dc_input_voltage_per_mpp})"
        )


if __name__ == '__main__':
    the_max_photovoltaic_string_length = MaxPhotoVoltaicStringLength()
    the_max_photovoltaic_string_length.main()
    # the_max_photovoltaic_string_length.main("photovoltaic_string_length_in.csv", "photovoltaic_string_length_out.csv")
