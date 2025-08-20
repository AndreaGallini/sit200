from ..concept import Measure

# durata dell'impianto
SYSTEM_LIFETIME = Measure("anno", 20.0)

# Fattori di emissioni per l’Italia
EFCO2 = Measure("kg CO2/kWh", 0.23)
EFCH4 = Measure("kg CH4/kWh", 0.015)
EFN2O = Measure("kg N2O/kWh", 0.0002)

# fattori di conversione in CO2 equivalente
CH4_CO2 = Measure("CH4/CO2", 28.0)
N2O_CO2 = Measure("N2O/CO2", 273.0)

# conversione standard in TEP
CTEP = Measure("kWh/TEP", 11630.0)
