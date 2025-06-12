"""
This script enriches a dataset of GPS points with country information by
mapping each (latitude, longitude) pair to a country using a GeoJSON file.

Steps:
1. Load country geometries from GeoJSON.
2. Load clustered GPS data from a CSV file.
3. Query the country for each coordinate pair using spatial containment.
4. Append country names to the data.
5. Filter out points with unknown locations.
6. Save the valid results to a new CSV file.
"""

import pandas as pd
import time
import requests  # Package for country query
from shapely.geometry import mapping, shape
from shapely.prepared import prep
from shapely.geometry import Point

# Load country boundaries from GeoJSON
data = requests.get("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson").json()
countries = {}
for feature in data["features"]:
    geom = feature["geometry"]
    country = feature["properties"]["ADMIN"]
    countries[country] = prep(shape(geom))

# Define function to map a coordinate to a country
def get_country(lon, lat):
    point = Point(lon, lat)
    for country, geom in countries.items():
        if geom.contains(point):
            return country
    return "unknown"

start = time.time()  # Start timing

file_path = r"D:\MLAP\PRT2\Test\Cellular.csv"
CELL1 = pd.read_csv(file_path)  # Load input data
CELL = CELL1.drop(labels=['Unnamed: 0'], axis=1)  # Drop index column if present

# Convert latitude and longitude columns to lists
lat = CELL['latitude']
lon = CELL['longitude']
latlist = lat.tolist()
lgtlist = lon.tolist()

# Query countries for all coordinate pairs
country = [get_country(int(lgtlist[i]), int(latlist[i])) for i in range(len(lat))]

# Append country information to the DataFrame
country_sr = pd.Series(country, index=lat.index)
CELL["land"] = pd.DataFrame(country_sr, columns=["land"])

# Remove entries with unknown country
CELL_nounknown = CELL[~CELL['land'].isin(["unknown"])]

# Save result to CSV
CELL_nounknown.to_csv('CELL_nounknown.csv', mode='a', index=None)

end = time.time()  # End timing
print("run time = {}".format(end - start))  # Print execution time
