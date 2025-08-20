import csv
import json
import re
import itertools
import os
from .utils import log

months = {
    'GEN': 31,
    'FEB': 28.25,
    'MAR': 31,
    'APR': 30,
    'MAG': 31,
    'GIU': 30,
    'LUG': 31,
    'AGO': 31,
    'SET': 30,
    'OTT': 31,
    'NOV': 30,
    'DIC': 31
}


def dict2text(d, unit=True):
    text = []
    for k, v in d.items():
        if isinstance(v, Measure):
            if unit:
                text.append(f"{k} = {v.value} {v.unit}")
            else:
                text.append(f"{k} = {v.value}")
        elif isinstance(v, dict):
            text2 = dict2text(v, unit)
            text.append(f"{k}:\n{text2}")
    return "\n".join(text)


def dictMeasure2dict(d, unit=False):
    """
    sostituiamo le misure con il mero valore
    """
    diz = {}
    #print("dictMeasure2dict", d)
    for k, v in d.items():
        if isinstance(v, Measure):
            if unit:
                diz[k] = (v.value, v.unit)
            else:
                diz[k] = v.value
        elif isinstance(v, dict):
            diz[k] = dictMeasure2dict(v, unit)
        elif isinstance(v, tuple):
            diz[k] = v
        elif isinstance(v, (float, str)):
            diz[k] = v
        else:
            #print("\n\n*** input was: ",k, v)
            log("ERROR", f"dictMeasure2dict: Unexpected situation! {type(v)}")
            return False
    return diz


class MonthlySolarDeclination:
    def __init__(self):
        monthlySolarDeclinationDataPath = os.path.join(os.path.dirname(__file__), 'data',
                                                       'monthly_solar_declination.json')
        with open(monthlySolarDeclinationDataPath) as f:
            self.declinations = json.load(f)

    def get_solar_declination(self, month):
        return self.declinations[month]


class ClimatePosition:
    climateStationDataPath = os.path.join(os.path.dirname(__file__), 'data',
                                          'climate_stations_position_temperature_irradiance.json')
    with open(climateStationDataPath, 'r') as file:
        climateStationData = json.load(file)

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.the_nearest_station = self.find_nearest_station()
        log("DEBUG", f"({self.latitude}, {self.longitude}) Nearest station: {self.the_nearest_station}")

    def find_nearest_station(self):
        min_distance = float('inf')
        nearest_station = None
        for station in self.climateStationData:
            station_lat, station_lon = station['Latitudine'], station['Longitudine']
            distance = ((self.latitude - station_lat) ** 2 + (self.longitude - station_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_station = station
        return nearest_station

    def find_two_nearest_stations_old(self):
        min_distance = float('inf')
        nearest_station = None
        second_nearest_station = None
        for station in self.climateStationData:
            station_lat, station_lon = station['Latitudine'], station['Longitudine']
            distance = ((self.latitude - station_lat) ** 2 + (self.longitude - station_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                second_nearest_station = nearest_station
                nearest_station = station
        return nearest_station, second_nearest_station

    def find_two_nearest_stations(self):
        log("DEBUG", f"({self.latitude}, {self.longitude}) Finding two nearest stations")
        min_upper_distance = float('inf')
        min_lower_distance = float('inf')
        top_station = None
        bottom_station = None
        for station in self.climateStationData:
            if bottom_station is None or bottom_station['Latitudine'] > station['Latitudine']:
                bottom_station = station
            if top_station is None or top_station['Latitudine'] < station['Latitudine']:
                top_station = station
        log("DEBUG", f"({self.latitude}, {self.longitude}) top station: {top_station}")
        log("DEBUG", f" ({self.latitude},{self.longitude}) bottom station: {bottom_station}")
        nearest_upper_station = top_station
        nearest_lower_station = bottom_station
        for station in self.climateStationData:
            station_lat, station_lon = station['Latitudine'], station['Longitudine']
            distance = ((self.latitude - station_lat) ** 2 + (self.longitude - station_lon) ** 2) ** 0.5
            if station_lat > self.latitude:
                if distance < min_upper_distance:
                    min_upper_distance = distance
                    nearest_upper_station = station
            else:
                if distance < min_lower_distance:
                    min_lower_distance = distance
                    nearest_lower_station = station
        log("DEBUG", f"({self.latitude}, {self.longitude}) nearest upper station: {nearest_upper_station}")
        log("DEBUG", f"({self.latitude}, {self.longitude}) nearest lower station: {nearest_lower_station}")
        return nearest_upper_station, nearest_lower_station

    def get_nearest_station(self):
        return self.the_nearest_station

    def get_month_avg_daily_temperature(self, month):
        return self.the_nearest_station[month]["Temperatura"]

    def get_month_avg_irradiance(self, month):
        return {
            "Irradianza_Totale": self.the_nearest_station[month]["Irradianza_Totale"],
            "Irradianza_Diffusa": self.the_nearest_station[month]["Irradianza_Diffusa"],
            "Irradianza_Diretta": self.the_nearest_station[month]["Irradianza_Diretta"]
        }


class Measure:
    def __init__(self, unit, value=None):
        self.unit = unit
        self.value = value

    def validate(self, unit, value_types):
        if self.unit == unit:
            if isinstance(value_types, type):
                if isinstance(self.value, value_types):
                    return True
                if isinstance(self.value, tuple) and isinstance(self.value, value_types):
                    return True
                log("ERROR", "wrong type value, expecting {}".format(value_types))
        else:
            log("ERROR", "Unit of measure must be of type '{}'".format(value_types))
        return False

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def dump(self):
        return f'{self.value} {self.unit}'

    def text(self):
        return f'{self.value} {self.unit}'

    def read_csv(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
        for row in data:
            for key, value in row.items():
                match = re.match(r"(-?\d*\.?\d+)\s*\((.*)\)", value)
                if match:
                    row[key] = (float(match.group(1)), match.group(2))
        return data[0] if len(data) == 1 else data

    def write_csv(seflf, filename, data):
        if isinstance(data, dict):
            data = [data]
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                formatted_row = {k: f"{v[0]} ({v[1]})" if isinstance(v, tuple) else v for k, v in row.items()}
                writer.writerow(formatted_row)

    def json(self):
        return json.dumps({'value': self.value, 'unit': self.unit})


class Classification:
    def __init__(self, classes_list):
        self.classes = classes_list

    def validate(self):
        if not isinstance(self.classes, list):
            return None
        for threshold in self.classes:
            if not isinstance(threshold, tuple):
                return None
            if len(threshold) == 2:
                threshold_value, threshold_name = threshold
                if not isinstance(threshold_value, float) or not isinstance(threshold_name, str):
                    return None
            elif len(threshold) == 3:
                threshold_value, threshold_name, threshold_comment = threshold
                if (not isinstance(threshold_value, float)
                        or not isinstance(threshold_name, str)
                        or not isinstance(threshold_comment, str)):
                    return None
            else:
                return None

    def classify(self, the_measure: Measure):
        if not isinstance(the_measure, Measure):
            return None
        the_value = the_measure.value
        the_class = self.classes[0]
        for class_cursor in self.classes:
            if len(class_cursor) == 2:
                threshold, class_name = class_cursor
            elif len(class_cursor) == 3:
                threshold, class_name, comment = class_cursor
            else:
                log("ERROR", "expected 2 or 3 elements, got {}".format(class_cursor))
                return None
            the_class = class_cursor
            if the_value < threshold:
                #print(the_value, threshold, "stop!")
                break
            else:
                pass
                #print(the_value, threshold, "next threshold...")
        return the_class


class MeasureDerivation:

    def __init__(self):
        self.input = {}
        self.output = {}

    def load_data(self, filename):
        if not open(filename, 'r').readlines():
            raise FileNotFoundError

    def validate_input(self, the_key, the_type, the_dict=None):
        if the_dict is None:
            the_dict = self.input
        if the_key not in the_dict:
            log("ERROR", f"{the_key} is not in input")
            return False
        the_value = the_dict[the_key]
        if isinstance(the_value, Measure):
            if the_value.unit != the_type:
                log("ERROR", f"{the_key} is not in {the_type}")
                return False
        elif isinstance(the_value, dict):
            for the_value_key, the_value_value in the_value.items():
                if not self.validate_input(the_value_key, the_type, the_value):
                    log("ERROR", f"an entry of {the_key} is not in {the_type}")
                    return False
        else:
            log("ERROR", f"{the_key} is not a Measure nor a dict")
            return False
        return True

    def validate(self):
        pass

    def compute(self):
        pass

    def dump(self):
        text = ""
        for k, v in itertools.chain(self.input.items(), self.output.items()):
            formatted_value = (
                f"{v.value}"
                if isinstance(v, Measure) and v.unit == 'bool'
                else f"{v:.2f}"
                if isinstance(v, (float, int))
                else "\n" + "\n".join(f"\t{kk}: {vv.dump() if isinstance(vv, Measure) else vv}" for kk, vv in v.items())
                if isinstance(v, dict)
                else "\n" + "\n".join(vv.dump() if isinstance(vv, Measure) else str(vv) for vv in v)
                if isinstance(v, list)
                else f"{v.value} {v.unit}"
                if isinstance(v, Measure)
                else str(v)
            )
            text += k.replace("_", " ") + ": " + formatted_value + "\n"
        return text

    def results(self):
        return self.output

    def json(self):
        all_the_values = json.dumps("")
        for k, v in itertools.chain(self.input.items(), self.output.items()):
            if isinstance(v, Measure):
                all_the_values = json.dumps({'value': v.value, 'unit': v.unit})
            elif isinstance(v, dict):
                all_the_values = {}
                # print("JSON...", v)
                try:
                    for key, measure in v.items():
                        # print(f"{key}: {value}")
                        if isinstance(measure, Measure):
                            single_value = json.dumps({'value': measure.value, 'unit': measure.unit})
                            all_the_values[key] = single_value
                            # print("JSON:", text)
                        else:
                            print(f"JSON: {measure} is not a Measure")
                except AttributeError:
                    log("ERROR", "this dict does not contains only Measure data")
        return all_the_values

    def text_deprecated(self):
        text = ""
        for k, v in itertools.chain(self.input.items(), self.output.items()):
            formatted_value = (
                f"{v.value}"
                if isinstance(v, Measure) and v.unit == 'bool'
                else f"{v:.2f}"
                if isinstance(v, (float, int))
                else "\n" + "\n".join(f"\t{kk}: {vv.dump() if isinstance(vv, Measure) else vv}" for kk, vv in v.items())
                if isinstance(v, dict)
                else "\n" + "\n".join(vv.dump() if isinstance(vv, Measure) else str(vv) for vv in v)
                if isinstance(v, list)
                else f"{v.value} {v.unit}"
                if isinstance(v, Measure)
                else str(v)
            )
            text += k.replace("_", " ") + ": " + formatted_value + "\n"
        return text

    def get_text(self, unit=True):
        """
        rappresentazione dell'output del modello, cioè l'esito della derivazione della misura
        """
        return dict2text(self.output, unit) + "\n"

    def get_output(self, unit=False):
        return dictMeasure2dict(self.output, unit)

    def main(self, the_input_data=None, the_input_csv=None, the_output_csv=None):
        self.validate()
        self.compute()
        return self.dump()
        # TODO: data csv --> csv
    #
    #     if the_input_data:
    #         self.input_data = the_input_data
    #         if self.validate():
    #             self.compute()
    #             return self.measurable_quantities['output']
    #         else:
    #             print('Input data not valid')
    #             return None
    #     elif the_input_csv and the_input_csv:
    #         self.measurable_quantities['input'] = tools.read_measurements(the_input_csv)
    #         if self.validate():
    #             self.compute()
    #             tools.write_measurements(the_output_csv, [
    #                 self.measurable_quantities['output']
    #             ])
    #             return None
    #         else:
    #             print("input data not valid")
    #             return None
    #     else:
    #         self.compute()
    #         for io in ['input', 'output']:
    #             for measurable_quantity, measurement in self.measurable_quantities[io].items():
    #                 value = measurement['value']
    #                 unit = measurement['unit']
    #                 label = measurable_quantity.replace('_', ' ')
    #                 print(f'{label}: {value} {unit}')


class MeasurableQuantity:
    def __init__(self, code, unit):
        self.code = code  # short string in english and snake case format
        self.unit = unit
        self.value = None

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class CalculationMethod:
    def __init__(self, code, input_quantities, output_quantities):
        self.code = code
        self.input_quantities = input_quantities
        self.output_quantities = output_quantities

    def calculate(self, input_values):
        pass
        raise NotImplementedError("The calculation method must be implemented in the subclasses")


class Calculation:
    def __init__(self, quantity, method=None, values=None):
        self.quantity = quantity
        self.method = method
        self.values = values

    def compute(self, input_values=None):
        if self.method:
            self.values = self.method.calculate(input_values)
        return self.values

    def validate(self):
        pass

    def main(self, the_input_data=None, the_input_csv=None, the_output_csv=None):
        pass
        '''
        if the_input_data:
            self.input_data = the_input_data
            if self.validate():
                self.compute()
                return self.measurable_quantities['output']
            else:
                print('Input data not valid')
                return None
        elif the_input_csv and the_input_csv:
            self.measurable_quantities['input'] = tools.read_measurements(the_input_csv)
            if self.validate():
                self.compute()
                tools.write_measurements(the_output_csv, [
                    self.measurable_quantities['output']
                ])
                return None
            else:
                print("input data not valid")
                return None
        else:
            self.compute()
            for io in ['input', 'output']:
                for measurable_quantity, measurement in self.measurable_quantities[io].items():
                    value = measurement['value']
                    unit = measurement['unit']
                    label = measurable_quantity.replace('_', ' ')
                    print(f'{label}: {value} {unit}')
        '''
