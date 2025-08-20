import csv
import os.path


class PhotovoltaicSystemArea:
    def __init__(self):
        self.panels_number = 0
        self.panel_width = 0.0 # m
        self.panel_height = 0.0 # m
        self.panel_area = 0.0 # m2
        self.system_area = 0.0 # ha

    def main(self, csvfile_in = None, csvfile_out = None):
        # set exemplary data o get data from a csv file and compute result
        if csvfile_in is None and csvfile_out is None:
            self.set_panels_number(200000)
            self.set_panel_width(1.0)
            self.set_panel_height(2.0)
            self.compute_system_area()
            self.output2display()
        elif os.path.isfile(csvfile_in):
            self.extract(csvfile_in)
            self.compute_system_area()
            self.output2csv()
        else:
            print('Please, input two valid csv files: the first one for input and the second one for output')
            print('The first one must exists. The second one, if exists, will be overwritten')

    def extract(self, the_csvfile_in):
        # extract data from csv file: number, width, height
        with open(the_csvfile_in, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            try:
                row = next(reader)
                try:
                    self.panels_number = int(row[0])
                    self.panel_width = float(row[1])
                    self.panel_height = float(row[2])
                except ValueError as e:
                    print(f"Please input a valid csv file, containing only integer data. Error: {e}")
            except StopIteration:
                print('Please input a not empty csv file with 3 columns: Number of Panels, single panel width and '
                      'single panel height')
                return None

    def output2display(self):
        # output computed result to console
        print(
            f"Number of Panels: {self.panels_number}"
            f"\nWidth of each Panel: {self.panel_width} m"
            f"\nHeight of each Panel: {self.panel_height} m"
            f"\nArea of each Panel: {self.panel_area} m2"
            f"\nSystem Area: {self.system_area} ha"
        )

    def output2csv(self):
        # output computed result to csv file
        csvfile = open("photovoltaic_system_area_out.csv", 'w')
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow([self.system_area])

    def compute_panel_area(self):
        self.panel_area = self.panel_height * self.panel_width

    def compute_system_area(self):
        # this is the core module!
        # input: Number of Panels, Width of each Panel (m) and Height of each Panel (m)
        self.compute_panel_area()
        self.system_area = self.panel_area * self.panels_number / 10000 # m2 => ha conversion

    def set_panels_number(self, the_panels_number):
        self.panels_number = the_panels_number

    def set_panel_width(self, the_panel_width):
        self.panel_width = the_panel_width

    def set_panel_height(self, the_panel_height):
        self.panel_height = the_panel_height

    def get_panel_area(self):
        self.compute_panel_area()
        return self.panel_area

    def get_system_area(self):
        return self.system_area


if __name__ == '__main__':
    the_system_area = PhotovoltaicSystemArea()
    the_system_area.main()
    #the_system_area.main("photovoltaic_system_area_in.csv", "photovoltaic_system_area_out.csv")
