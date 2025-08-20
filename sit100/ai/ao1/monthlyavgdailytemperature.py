# Arancione SOLE 1 Temperatura giornaliera media mensile
# input: latitudine e longitudine
# output: temperature UNI 10349 giornaliere medie mensili mese per mese della stazione climatica più vicina

from .concept import Measure, MeasureDerivation, ClimatePosition, months


class MonthlyAvgDailyTemperature(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        try:
            self.input = {
                'latitude': the_input_data['latitude'],
                'longitude': the_input_data['longitude']
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'monthly_avg_daily_temperature': {}
        }

    def validate(self):
        if self.input['latitude'] is None or self.input['longitude'] is None:
            return False
        if not isinstance(self.input['latitude'], Measure):
            return False
        if not isinstance(self.input['longitude'], Measure):
            return False
        return True

    def compute(self):
        position = ClimatePosition(self.input['latitude'].value, self.input['longitude'].value)
        station = position.get_nearest_station()
        monthly_avg_daily_temperature = {}
        for month in months:
            monthly_avg_daily_temperature[month] = Measure("°C", round(station[month]['Temperatura'], 2))
        self.output['monthly_avg_daily_temperature'] = monthly_avg_daily_temperature


if __name__ == '__main__':
    the_target = MonthlyAvgDailyTemperature({
        "latitude": Measure("°", 45.67),
        "longitude": Measure("°", 12.24)
    })
    if the_target.validate():
        print(the_target.main())
    else:
        print("input not valid, error")
        print(the_target.dump())
