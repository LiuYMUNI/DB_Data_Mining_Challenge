"""
This script processes GNSS signal data to generate a heatmap using Folium.
It filters high-quality HDOP-based positions, calculates signal quality,
and visualizes the data as a geographic heatmap.

Steps:
1. Load the input data.
2. Filter rows where position was determined via GNSS (type 1).
3. Drop irrelevant columns and keep only high-quality signals (HDOP ≤ 35).
4. Map signal quality inversely to HDOP.
5. Create and display a heatmap using Folium.
"""

import pandas as pd
import numpy as np
import gc
import time
import requests
import folium
from folium.plugins import HeatMap

start = time.time()  # Start timing

# Load the dataset and filter for GNSS-based localization
table1 = pd.read_csv(r"D:\MLAP\PRT2\Test\02_211203_TUDA_data11.csv", index_col='wagon_ID')
table2 = table1[table1['determination_position'].isin([1])]
del table1
gc.collect()

# Drop unnecessary columns
table3 = table2.drop(labels=[
    'loading_state', 'loading_state_update', 'altitude',
    'signal_quality_satellite', 'determination_position', 'GNSS_velocity',
    'timestamp_measure_position', 'timestamp_transfer',
    'movement_state', 'timestamp_measure_movement_state',
    'timestamp_index', 'provider'
], axis=1)
del table2
gc.collect()

# Filter signals with good HDOP (≤ 35)
table_goodsignal = table3[table3['signal_quality_hdop'] <= 35]
table_goodsignal.loc[:, 'signal_quality'] = 35 - table_goodsignal['signal_quality_hdop']
lat2 = table_goodsignal['latitude']
lon2 = table_goodsignal['longitude']
quality = table_goodsignal["signal_quality"]
del table_goodsignal
gc.collect()

# Create DataFrame for heatmap
dict2 = {'lat': lat2.values, 'lon': lon2.values, "quality": quality.values}
df_lat_lon = pd.DataFrame(dict2, index=lat2.index)
del lat2, lon2, quality, dict2
gc.collect()

# Convert to list for Folium
final = df_lat_lon.to_numpy().tolist()
del df_lat_lon
gc.collect()

# Generate HeatMap
m = folium.Map([52.12, 9.74], tiles='OpenStreetMap', zoom_start=6)
HeatMap(final, min_opacity=0.3, radius=14.5, blur=10).add_to(m)

# Save map to file
output_file = '111111.html'
m.save(output_file)

end = time.time()  # End timing
print("run time = {}".format(end - start))
