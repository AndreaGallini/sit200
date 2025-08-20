# Arancione SOLE 2 Temperatura giornaliera media annua
# input: latitudine e longitudine
# output: temperature UNI 10349 media annua della stazione climatica più vicina

from .concept import Measure, MeasureDerivation, ClimatePosition

class AnnualAvgTemperature(MeasureDerivation):
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
            'avg_annual_temperature': Measure("°", 0.0)
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
        self.output['avg_annual_temperature'] = Measure("°", station['MEDIA ANNUA'])


if __name__ == '__main__':
    the_target = AnnualAvgTemperature({
        "latitude": Measure("°", 41.9028),
        "longitude": Measure("°", 12.4964)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
