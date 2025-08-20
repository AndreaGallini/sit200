# TODO: racchiudere il codice principale in una classe
# TODO: spostare i test ciascuno in un file a sé nella cartella tests
# TODO: spezzare la funzione in parte input da csv e parte output a csv

import pytest
import csv
import tempfile

annual_production = 13000  # kWh
conversion_factor_tep = 0.000187  # tep/kWh (ARERA value)
plant_lifetime = 25  # years
gas_conversion_factor = 0.09  # tep/m³
gas_heating_value = 9.5  # kWh/m³
plant_area = 5  # hectares
biodiversity_loss = 40  # %
reforestation_rate = 0.2  # ha/year


def emissions_per_kwh(the_energy_mix, the_emission_factors):
    """Calculates emissions mix (CO2, SO2, NOx, and PM) per kWh of electricity."""
    emissions_mix = {'CO2': 0, 'SO2': 0, 'NOx': 0, 'PM': 0}
    for source, percentage in the_energy_mix.items():
        for pollutant, factor in the_emission_factors[source].items():
            emissions_mix[pollutant] += percentage * factor
    return emissions_mix


def tep_saved(the_annual_production, conversion_factor, the_plant_lifetime):
    """Calculates the total TEP saved over the plant's lifetime."""
    return (the_annual_production / 1000) * conversion_factor * the_plant_lifetime


def natural_gas_saved(the_tep_saved, the_gas_conversion_factor, the_gas_heating_value):
    """Calculates the volume of natural gas saved, given the savings in TEP."""
    energy_equivalent_gas = the_tep_saved / the_gas_conversion_factor
    return energy_equivalent_gas * the_gas_heating_value


def annual_reforestation(the_plant_area, the_biodiversity_loss, the_reforestation_rate):
    """Calculates the annual equivalent reforestation for a PV plant."""
    return (the_plant_area * the_biodiversity_loss / 100) / the_reforestation_rate


def process_emissions_data(input_filename="emissions_data.csv", output_filename="results.csv"):
    """
    Processes emissions data from a CSV file and calculates various metrics, then saves the results to a new CSV file.

    Args:
        input_filename (str): Name of the input CSV file.
        output_filename (str): Name of the output CSV file.
    """

    with open(input_filename, 'r', newline='') as infile, open(output_filename, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)  # Read CSV as a dictionary of rows
        writer = csv.writer(outfile)  # Write CSV with just values

        header = [
            'CO2 emissions (g/kWh)', 'SO2 emissions (g/kWh)', 'NOx emissions (g/kWh)', 'PM emissions (g/kWh)',
            'TEP saved', 'Natural gas saved (m³)', 'Annual reforestation (ha/year)'
        ]
        writer.writerow(header)  # Write the header row

        for row in reader:
            the_energy_mix = {source: float(row[source]) for source in ['renewable', 'fossil', 'nuclear']}
            the_emission_factors = {
                source: {pollutant: float(row[f"{source}_{pollutant}"]) for pollutant in ['CO2', 'SO2', 'NOx', 'PM']}
                for source in ['renewable', 'fossil', 'nuclear']
            }
            the_annual_production = float(row['annual_production_kwh'])
            the_plant_lifetime = float(row['plant_lifetime_years'])
            the_plant_area = float(row['plant_area_hectares'])
            the_biodiversity_loss = float(row['biodiversity_loss_percent'])
            the_reforestation_rate = float(row['reforestation_rate_ha_year'])

            the_emissions = emissions_per_kwh(the_energy_mix, the_emission_factors)
            the_tep_saved_total = tep_saved(the_annual_production, conversion_factor_tep, the_plant_lifetime)
            the_gas_saved = natural_gas_saved(the_tep_saved_total, gas_conversion_factor, gas_heating_value)
            the_reforestation = annual_reforestation(the_plant_area, the_biodiversity_loss, the_reforestation_rate)

            writer.writerow(
                [the_emissions[pollutant] for pollutant in ['CO2', 'SO2', 'NOx', 'PM']] + [the_tep_saved_total,
                                                                                           the_gas_saved,
                                                                                           the_reforestation])


# Example usage
process_emissions_data()

# Example usage
energy_mix = {'renewable': 0.3, 'fossil': 0.6, 'nuclear': 0.1}
emission_factors = {
    'renewable': {'CO2': 0, 'SO2': 0, 'NOx': 0, 'PM': 0},
    'fossil': {'CO2': 500, 'SO2': 1, 'NOx': 2, 'PM': 0.5},
    'nuclear': {'CO2': 10, 'SO2': 0.1, 'NOx': 0.2, 'PM': 0.05}
}


# Calculate emissions, TEP saved, gas saved, and reforestation
emissions = emissions_per_kwh(energy_mix, emission_factors)
tep_saved_total = tep_saved(annual_production, conversion_factor_tep, plant_lifetime)
gas_saved = natural_gas_saved(tep_saved_total, gas_conversion_factor, gas_heating_value)
reforestation = annual_reforestation(plant_area, biodiversity_loss, reforestation_rate)

print("Emissions per kWh:", emissions)
print("TEP saved:", tep_saved_total)
print("Natural gas saved (m³):", gas_saved)
print("Annual equivalent reforestation (ha/year):", reforestation)


# ... (same functions as before: emissions_per_kwh, tep_saved, natural_gas_saved, annual_reforestation)



# Test cases for emissions_per_kwh


def test_emissions_per_kwh_fossil():
    the_energy_mix = {'renewable': 0, 'fossil': 1.0, 'nuclear': 0}
    the_emissions = emissions_per_kwh(the_energy_mix, emission_factors)
    assert the_emissions == emission_factors['fossil']


def test_emissions_per_kwh_mixed():
    emission_output = emissions_per_kwh(energy_mix, emission_factors)
    assert emission_output['CO2'] == pytest.approx(301, abs=0.1)  # Allowing for slight rounding errors


# Test cases for tep_saved, natural_gas_saved, annual_reforestation
def test_tep_saved():
    assert tep_saved(13000, 0.000187, 25) == pytest.approx(60.875, abs=0.001)


def test_natural_gas_saved():
    assert natural_gas_saved(60.875, 0.09, 9.5) == pytest.approx(6450, abs=1)


def test_annual_reforestation():
    assert annual_reforestation(5, 40, 0.2) == 10


def test_process_emissions_data():
    # Create a temporary CSV file for testing
    with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False) as temp_csv:
        writer = csv.writer(temp_csv)
        writer.writerow([
            'renewable', 'fossil', 'nuclear',
            'renewable_CO2', 'renewable_SO2', 'renewable_NOx', 'renewable_PM',
            'fossil_CO2', 'fossil_SO2', 'fossil_NOx', 'fossil_PM',
            'nuclear_CO2', 'nuclear_SO2', 'nuclear_NOx', 'nuclear_PM',
            'annual_production_kwh', 'plant_lifetime_years', 'plant_area_hectares',
            'biodiversity_loss_percent', 'reforestation_rate_ha_year'
        ])
        writer.writerow([0.3, 0.6, 0.1, 0, 0, 0, 0, 500, 1, 2, 0.5, 10, 0.1, 0.2, 0.05, 13000, 25, 5, 40, 0.2])
    temp_csv_filename = temp_csv.name

    # Call the function to process the temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False) as temp_output_csv:
        output_filename = temp_output_csv.name
        process_emissions_data(temp_csv_filename, output_filename)

    # Read the generated results file
    with open(output_filename, 'r', newline='') as result_file:
        reader = csv.reader(result_file)
        next(reader)  # Skip the header row
        results = list(reader)[0]

    # Check if the results match the expected values
    expected_results = ['301.0', '0.61', '1.22', '0.305', '60.875', '6450.0', '10.0']
    assert results == expected_results
