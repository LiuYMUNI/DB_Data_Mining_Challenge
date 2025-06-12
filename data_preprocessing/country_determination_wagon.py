"""
This script performs geospatial analysis on railway wagon location data.
It reads timestamped GPS data, calculates distances between consecutive points,
determines average and median locations for each wagon, maps them to country names,
and exports the results.

Steps include:
1. Reading and cleaning the data.
2. Calculating haversine distance between points.
3. Grouping by wagon ID to compute mean/median positions.
4. Using geojson to determine the country of each wagon based on average/median position.
5. Writing the results to CSV.
"""

import pandas as pd
from math import radians, cos, sin, asin, sqrt
import time
import gc
import requests  # For address lookup

from shapely.geometry import mapping, shape  # For address lookup
from shapely.prepared import prep            # For address lookup
from shapely.geometry import Point           # For address lookup

# Load GeoJSON for country borders
data = requests.get("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson").json()
countries = {}
for feature in data["features"]:
    geom = feature["geometry"]
    country = feature["properties"]["ADMIN"]
    countries[country] = prep(shape(geom))

# Get country name from longitude and latitude
def get_country(lon, lat):
    point = Point(lon, lat)
    for country, geom in countries.items():
        if geom.contains(point):
            return country
    return "unknown"

start = time.time()  # Start timing
file_path = r"D:\MLAP\PRT2\Test\02_211203_TUDA_data.csv"
longterm = pd.read_csv(file_path)

# Sort by timestamp
lonterm_01 = longterm.sort_values(by='timestamp_measure_position')
del longterm
gc.collect()

# Create next-latitude/longitude columns for distance calculation
lonterm_01['lat_next'] = lonterm_01.groupby(['wagon_ID', 'loading_state'])['latitude'].shift(-1)
lonterm_01['lon_next'] = lonterm_01.groupby(['wagon_ID', 'loading_state'])['longitude'].shift(-1)

# Remove rows with NaNs
lonterm_01_nona = lonterm_01.dropna()
del lonterm_01
gc.collect()

# Haversine distance function
def Dis(series):
    lon1 = series["longitude"]
    lat1 = series["latitude"]
    lat2 = series["lat_next"]
    lon2 = series["lon_next"]
    lon1, lat1, lon2, lat2 = map(radians, map(float, [lon1, lat1, lon2, lat2]))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth radius in kilometers
    Dis = c * r
    return Dis

# Apply distance calculation
lonterm_01_nona['Dis'] = lonterm_01_nona.agg(Dis, axis=1)

df2 = lonterm_01_nona
del lonterm_01_nona
gc.collect()

# Group distances by wagon ID
df2_grouped = df2['Dis'].groupby(df2['wagon_ID'])

# Compute mean and median latitude/longitude per wagon
lat1 = df2['latitude'].groupby(df2['wagon_ID']).mean()
lon1 = df2['longitude'].groupby(df2['wagon_ID']).mean()
lat2 = df2['latitude'].groupby(df2['wagon_ID']).median()
lon2 = df2['longitude'].groupby(df2['wagon_ID']).median()

del df2
gc.collect()

# Create dataframe from mean values
dict1 = {'lat': lat1.values, 'lon': lon1.values}
df_lat_lon_mean = pd.DataFrame(dict1, index=lat1.index)
lat = lat1.tolist()
lgt = lon1.tolist()
country_mean = [get_country(int(lgt[i]), int(lat[i])) for i in range(len(lat))]
country_mean_sr = pd.Series(country_mean, index=lat1.index)
del country_mean
gc.collect()
df_lat_lon_mean["land"] = pd.DataFrame(country_mean_sr, columns=["land"])
df_lat_lon_mean.to_csv('mean.csv', mode='a')

# Create dataframe from median values
dict2 = {'lat': lat2.values, 'lon': lon2.values}
df_lat_lon_median = pd.DataFrame(dict2, index=lat2.index)
lat = lat2.tolist()
lgt = lon2.tolist()
country_median = [get_country(int(lgt[i]), int(lat[i])) for i in range(len(lat2))]
country_median_sr = pd.Series(country_median, index=lat2.index)
del country_median
gc.collect()
df_lat_lon_median["land"] = pd.DataFrame(country_median_sr, columns=["land"])
df_lat_lon_median.to_csv('median.csv', mode='a')

end = time.time()  # End timing
print("run time = {}".format(end - start))
