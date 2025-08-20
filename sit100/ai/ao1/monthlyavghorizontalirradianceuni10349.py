# arancione SOLE 5a Radiazione solare giornaliera media mensile al suolo su piano orizzontale UNI 10349

from .concept import Measure, MeasureDerivation, ClimatePosition, months
from .utils import log


class MonthlyAvgHorizontalIrradianceUni10349(MeasureDerivation):
    def __init__(self, the_input_data=None):
        super().__init__()
        self.system_loss = None
        try:
            self.input = {
                #'monthly_avg_daily_diffuse_horizontal_irradiance':
                #    the_input_data['monthly_avg_daily_diffuse_horizontal_irradiance'],
                #'monthly_avg_daily_beam_horizontal_irradiance':
                #    the_input_data['monthly_avg_daily_beam_horizontal_irradiance'],
                'latitude': the_input_data['latitude'],
                'longitude': the_input_data['longitude'],
            }
        except KeyError:
            print("missing input value")
            quit()
        self.output = {
            'monthly_avg_daily_horizontal_irradiance': {},
            'monthly_avg_daily_diffuse_horizontal_irradiance': {},
            'monthly_avg_daily_beam_horizontal_irradiance': {}
        }

    def validate(self):
        '''
        for key in self.input:
            for month in months:
                if month not in self.input[key]:
                    print("missing month in input")
                    return False
                if not isinstance(self.input[key][month], Measure):
                    print("input value is not a Measure")
                    return False
        '''
        if not isinstance(self.input['latitude'], Measure):
            print("latitude is not a Measure")
            return False
        if not isinstance(self.input['longitude'], Measure):
            print("longitude is not a Measure")
            return False
        return True

    def compute(self):
        log("DEBUG", f"{self.__class__.__name__} measure derivation model")

        def interpolate(irr1, irr2, lat1, lat2, lat):
            log("DEBUG", f"{self.__class__.__name__} interpolate {irr1} {irr2} {lat1} {lat2} {lat}")
            if lat1 == lat2:
                return irr1
            else:
                return irr1 + (irr2 - irr1) * (lat - lat1) / (lat2 - lat1)

        latitude = self.input['latitude'].value
        longitude = self.input['longitude'].value
        log("DEBUG", f"lat. {latitude}, long. {longitude}")
        position = ClimatePosition(latitude, longitude)
        nearest_station1, nearest_station2 = position.find_two_nearest_stations()
        position1 = ClimatePosition(nearest_station1['Latitudine'], nearest_station1['Longitudine'])
        lat1 = nearest_station1['Latitudine']
        name1 = nearest_station1['Provincia']
        log("DEBUG", f"Nearest station 1: {name1}, lat. {lat1}, long. {nearest_station1['Longitudine']}")
        position2 = ClimatePosition(nearest_station2['Latitudine'], nearest_station2['Longitudine'])
        lat2 = nearest_station2['Latitudine']
        name2 = nearest_station2['Provincia']
        log("DEBUG", f"Nearest station 2: {name2}, lat. {lat2}, long. {nearest_station2['Longitudine']}")
        for month in months:
            log("DEBUG", f"{month} irradiance calculations")
            irr1 = position1.get_month_avg_irradiance(month)
            irr1_tot = irr1['Irradianza_Totale']
            irr1_dif = irr1['Irradianza_Diffusa']
            irr1_dir = irr1['Irradianza_Diretta']
            log("DEBUG", f"irr1: {irr1}")
            irr2 = position2.get_month_avg_irradiance(month)
            irr2_tot = irr2['Irradianza_Totale']
            irr2_dif = irr2['Irradianza_Diffusa']
            irr2_dir = irr2['Irradianza_Diretta']
            log("DEBUG", f"irr2: {irr2}")
            irr_tot = round(interpolate(irr1_tot, irr2_tot, lat1, lat2, latitude), 2)
            log("DEBUG", f"irr_tot: {irr_tot}")
            irr_dif = round(interpolate(irr1_dif, irr2_dif, lat1, lat2, latitude), 2)
            log("DEBUG", f"irr_dif: {irr_dif}")
            irr_dir = round(interpolate(irr1_dir, irr2_dir, lat1, lat2, latitude), 2)
            log("DEBUG", f"irr_dir: {irr_dir}")
            self.output['monthly_avg_daily_horizontal_irradiance'][month] = Measure("kWh/m2", irr_tot)
            self.output['monthly_avg_daily_diffuse_horizontal_irradiance'][month] = Measure("kWh/m2", irr_dif)
            self.output['monthly_avg_daily_beam_horizontal_irradiance'][month] = Measure("kWh/m2", irr_dir)
            log("DEBUG", f"{month}, {name1}: dif {irr1_dif} + dir {irr1_dir} = tot {irr1_tot}")
            log("DEBUG", f"{month}, {name2}: dif {irr2_dif} + dir {irr2_dir} = tot {irr2_tot}")
            log("DEBUG", f"{month}, interp: dif {irr_dif} + dir {irr_dir} = tot {irr_tot}")


if __name__ == '__main__':
    the_target = MonthlyAvgHorizontalIrradianceUni10349({
        "latitude": Measure("°", 45.67),
        "longitude": Measure("°", 12.24)
    })
    if the_target.validate():
        the_target.main()
        print(the_target.dump())
    else:
        print("input not valid, error")
        print(the_target.dump())
