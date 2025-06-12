"""
This script visualizes GNSS data as a heatmap using Folium.
It reads a CSV file containing latitude, longitude, and signal quality data,
then generates a geographical heatmap of signal intensity.

Steps:
1. Read data from CSV.
2. Extract latitude, longitude, and quality.
3. Create a Folium map with HeatMap overlay.
4. Save the map as an HTML file and open it in the browser.
"""

import numpy as np
import pandas as pd
import gc
from math import radians, cos, sin, asin, sqrt
import time
import requests
import folium
import os
import webbrowser
from folium.plugins import HeatMap

start = time.time()  # Start timing

# Load the GNSS signal data
goodsignal1 = pd.read_csv(r"E:\sid\TU Darmstadt\Module und Lehrveranstaltungen\WS2022\MLA practical\Maschen_211207_TUDA_data.csv")

# Extract latitude, longitude, and signal quality
lat2 = goodsignal1['latitude']
lon2 = goodsignal1['longitude']

# ⚠️ Potential fix: replace with actual quality column if it exists
quality = goodsignal1["longitude"]  # ← replace with 'signal_quality' if that's correct

# Prepare data for heatmap
df_lat_lon = pd.DataFrame({'lat': lat2.values, 'lon': lon2.values, 'quality': quality.values}, index=lat2.index)
del lat2, lon2, quality
gc.collect()

# Convert to list for Folium
array = df_lat_lon.to_numpy()
final = array.tolist()
del array, df_lat_lon
gc.collect()

# Create and populate Folium map
m = folium.Map([52.12, 9.74], tiles='OpenStreetMap', zoom_start=6)
HeatMap(final, min_opacity=0.3, radius=14.5, blur=10).add_to(m)

# Save and open the heatmap
output_file = 'Maschen.html'
m.save(output_file)
webbrowser.open(output_file, new=2)

end = time.time()  # End timing
print("run time = {}".format(end - start))
