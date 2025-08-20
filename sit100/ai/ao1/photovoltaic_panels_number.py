import csv
import os.path


class PhotovoltaicPanelsNumber:
    def __init__(self):
        self.panels_number = 0
        self.panels_rated_power = 0 # W
        self.design_capacity = 0 # wWp

    def main(self, csvfile_in = None, csvfile_out = None):
        # use default data o get data from a csv file and compute result
        if csvfile_in is None and csvfile_out is None:
            self.set_panels_rated_power(400)
            self.set_design_capacity(10)
            self.compute_panels_number()
            self.output2display()
        elif os.path.isfile(csvfile_in):
            self.extract(csvfile_in)
            self.compute_panels_number()
            self.output2csv()
        else:
            print('Please input two valid csv files: the first one for input and the second one for output')
            print('The first one must exists. The second one, if exists, will be overwritten')

    def extract(self, the_csvfile_in):
        # extract data from csv file
        with open(the_csvfile_in, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            try:
                row = next(reader)
                try:
                    self.panels_rated_power = int(row[0])
                    self.design_capacity = int(row[1])
                except ValueError as e:
                    print(f"Please input a valid csv file, containing only integer data. Error: {e}")
            except StopIteration:
                print('Please input a not empty csv file with 2 columns: Panels rated power and Design Capacity')
                return None

    def output2display(self):
        # output computed result to console
        print(
            f"Design capacity: {self.design_capacity} kWp"
            f"\nPanels rated power: {self.panels_rated_power} W"
            f"\nNumber of Panels: {self.get_panels_number()}"
        )

    def output2csv(self):
        # output computed result to csv file
        csvfile = open("photovoltaic_panels_number_out.csv", 'w')
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow([self.panels_number])

    def compute_panels_number(self):
        # this is the core module!
        # input: Design capacity (kWp), Panels rated power (W); output: Number of panels
        self.panels_number = -(-self.design_capacity*1000//self.panels_rated_power)

    def set_panels_rated_power(self, the_panels_rated_power):
        self.panels_rated_power = the_panels_rated_power

    def set_design_capacity(self, the_design_capacity):
        self.design_capacity = the_design_capacity

    def get_panels_number(self):
        self.compute_panels_number()
        return self.panels_number


if __name__ == '__main__':
    pv = PhotovoltaicPanelsNumber()
    pv.main()
    pv.main("photovoltaic_panels_number_in.csv", "photovoltaic_panels_number_out.csv")
