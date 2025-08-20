# O3 yearly energy yield

import utils


class YearlyEnergyYield:
    def __init__(self, the_input_data=None):
        self.input_data = the_input_data if the_input_data else {}
        # Hardcoded example data go here
        self.nameplate_capacity = 5  # MW
        self.peak_sun_hours = 4  # hours by day
        self.efficiency = 0.75
        self.yearly_energy_yield = 5475  # MW

    def compute(self):
        self.yearly_energy_yield = self.nameplate_capacity * self.peak_sun_hours * 365 * self.efficiency

    def validate(self):
        data_schema = [
            int,
            int,
            float
        ]
        return tools.validate(self.input_data, data_schema)

    def main(self, the_input_data=None, the_input_csv=None, the_output_csv=None):
        if the_input_data:
            self.input_data = the_input_data
            if self.validate():
                self.compute()
                return [self.nameplate_capacity, self.peak_sun_hours, self.efficiency, self.yearly_energy_yield]
            else:
                print('Input data not valid')
                return None
        elif the_input_csv and the_input_csv:
            self.input_data = tools.read_csv_data(the_input_csv)
            if self.validate():
                self.compute()
                tools.write_csv_data(the_output_csv, [
                    self.nameplate_capacity,
                    self.peak_sun_hours,
                    self.efficiency,
                    self.yearly_energy_yield
                ])
                return None
            else:
                print("input data not valid")
                return None
        else:
            self.compute()
            print(
                f"system power: {self.nameplate_capacity}\n"
                f"peak sun hours: {self.peak_sun_hours}\n"
                f"efficiency: {self.efficiency}\n"
                f"yearly energy yield: {self.yearly_energy_yield}"
            )


if __name__ == '__main__':
    the_target = YearlyEnergyYield()
    the_target.main()
