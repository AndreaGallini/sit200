import csv
import datetime

import logging

logger = logging.getLogger('django')
'''
the_logger = logging.getLogger("cashflow")
the_logger.setLevel(logging.INFO)
logfile_handler = logging.FileHandler("cashflow.log")
logfile_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logfile_handler.setFormatter(formatter)
the_logger.addHandler(logfile_handler)
'''


def log(level, message):
    if level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.critical(message)
    else:
        logger.info(message + " (logging level NOT SET)")


class MeasurableQuantity:
    def __init__(self, description, units_of_measurement):
        self.description = description
        self.units_of_measurement = units_of_measurement


class Model:
    def __init__(self, name, source, measurable_quantities):
        self.name = name
        self.source = source
        self.measurable_quantities = measurable_quantities  # list


def read_csv_data(filename, single_row=True):
    """ if single row Read data from a CSV file and return a list."""
    """ else read data from a CSV file and return a list of lists."""
    data = []
    with open(filename, 'r', newline='') as csvfile:
        if single_row:
            # TODO: verify if it is better to use dict, so first row must be header
            #     reader = csv.DictReader(csvfile)
            reader = csv.reader(csvfile, delimiter=',')
            return list(reader)
        else:
            reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            data.append(row)
        return data


def write_csv_data(filename, data, the_header=None):
    with open(filename, 'w', newline='') as csvfile:
        if the_header or (isinstance(data, list) and isinstance(data[0], dict)):
            if not the_header:
                the_header = data[0].keys()
            writer = csv.DictWriter(
                csvfile, fieldnames=the_header, delimiter=';')
            writer.writeheader()
        else:
            writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(data)


def validate(input_data, data_schema):
    print("validate", input_data)
    # validate a dictionary of input data against a list of types (int or float)
    # try to convert data from string to int or float
    if not isinstance(input_data, dict):
        print('Input data must be a dictionary')
        return False
    if len(input_data) != len(data_schema):
        print(
            f"expecting {len(data_schema)} parameters, got {len(input_data)}")
        return False
    # TODO: prune this branch after adapting models, accept only dict
    if isinstance(data_schema, list):
        for i, v in enumerate(input_data.values()):
            t = data_schema[i]
            if t == int:
                try:
                    v = int(v)
                except ValueError:
                    print(
                        f"expecting integer values for {t} parameter, got {v}")
                    return False
            elif t == float:
                try:
                    v = float(v)
                except ValueError:
                    print(f"expecting float values for {t} parameter, got {v}")
                    return False
    elif isinstance(data_schema, dict):
        for k, v in input_data.items():
            t = data_schema[k]
            if t == int:
                try:
                    v = int(v)
                except ValueError:
                    print(
                        f"expecting integer values for {t} parameter, got {v}")
                    return False
            elif t == float:
                try:
                    v = float(v)
                except ValueError:
                    print(f"expecting float values for {t} parameter, got {v}")
                    return False
            else:
                return False
    return True


def proper_round(num, decimals=0):
    return round(num, decimals)


def write_measurements(dictionary, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(dictionary.values())
        csvfile.close()
        return dictionary


def read_measurements(filename):
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        dictionary = {}
        for row in reader:
            dictionary[row[0]] = {'value': row[1], 'units': row[2]}
        return dictionary


def validate_input(input_data, data_schema):
    # validate measures in the form measurable_quantity_name: { "value": the_value, "unit": the_unit }
    # TODO: check length, name of measurable_quantities, type of value, unit of measurement
    return True


capacities = [17.5, 20, 30, 38, 53, 71, 94, 117, 148, 185,
              222, 260, 300, 341, 407, 740, 925, 1110, 1295, 1480, 1665]


def cable_section_by_capacity(capacity):
    sections = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95,
                120, 150, 185, 240, 280, 350, 420, 490, 560, 630]
    for i, cap in enumerate(capacities):
        if cap < capacity:
            i += 1
        else:
            return capacities[i], sections[i]
    return 0, 0


def cable_resistance_by_capacity(capacity):
    resistances = [14.800, 8.910, 5.570, 3.710, 2.240, 1.410, 0.889, 0.641, 0.473, 0.328, 0.236, 0.188, 0.153, 0.123,
                   0.094, 0.082, 0.066, 0.055, 0.047, 0.041, 0.036]
    for i, cap in enumerate(capacities):
        if cap < capacity:
            i += 1
        else:
            return capacities[i], resistances[i]
    return 0, 0
