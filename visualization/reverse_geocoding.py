"""
This script performs reverse geocoding on GPS data using the Nominatim service from OpenStreetMap.
It reads a CSV containing latitude and longitude columns, converts them into location strings,
and retrieves full address information for each coordinate.

Steps:
1. Load one CSV file from the specified folder.
2. Generate "latitude,longitude" strings.
3. Perform reverse geocoding using geopy with a rate limiter.
4. Parse and split address strings into structured columns.
5. Print or optionally save the structured result.
"""

import pandas as pd
import glob
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import plotly_express as px
from tqdm import tqdm

# Path to folder containing 45 long-term CSVs
file_path = r"D:\MLAP\PRT2\Test\*.csv"
csv_list = glob.glob(file_path)

# Load the first CSV file
with open(csv_list[0]) as f:
    df = pd.read_csv(f)

# Create 'latitude,longitude' strings
df["geom"] = df["latitude"].map(str) + ',' + df["longitude"].map(str)

# Initialize geocoder and rate limiter
locator = Nominatim(user_agent="myGeocoder", timeout=10)
rgeocode = RateLimiter(locator.reverse, min_delay_seconds=0.001)

# Apply reverse geocoding with progress bar
tqdm.pandas()
df["address"] = df["geom"].progress_apply(rgeocode)

# Convert address results into a string for splitting
df["address_str"] = df["address"].astype(str)

# Create a new DataFrame splitting the address into components
address_components = df["address_str"].str.split(",", expand=True)

# Concatenate original index or dummy column with address components
result = pd.concat([df[["latitude", "longitude"]], address_components], axis=1)

# Print sample result
print(result.head())

# Optional: save result
# result.to_csv("reverse_geocoded_addresses.csv", index=False)
