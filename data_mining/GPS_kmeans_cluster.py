"""
This script performs KMeans clustering on GPS data (latitude and longitude) 
from railway wagons. It calculates cluster groupings and saves the average 
signal quality per cluster.

Steps:
1. Load preprocessed CSV containing GPS and signal quality data.
2. Drop irrelevant columns and extract latitude/longitude features.
3. Run KMeans clustering (2000 clusters).
4. Append cluster labels back to the original data.
5. Compute average quality metrics for each cluster and save to CSV.
"""

import matplotlib.pyplot as plt
from sklearn.datasets._samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score
import pandas as pd
import time
import numpy as np
from joblib import parallel_backend
import gc

start = time.time()  # Start timing

# Read preprocessed data, indexed by 'wagon_ID'
data = pd.read_csv(r"D:\MLAP\PRT2\goodsignalaccel35.csv", index_col='wagon_ID')

# Keep only latitude, longitude, and quality
data = data.drop(labels=['timestamp_index', 't_measure', 'time_delta', 't_transfer'], axis=1)

# Extract latitude and longitude
x = data.iloc[:, :2]

# Run KMeans clustering with 2000 clusters
mod = KMeans(n_clusters=2000, random_state=42)
y_pre = mod.fit_predict(x)

end = time.time()  # End timing
print("run time = {}".format(end - start))  # Print execution time

del x
gc.collect()

# Create DataFrame of cluster labels
labels = pd.DataFrame(mod.labels_)
labels.index = data.index
labels.rename(columns={0: 'group'}, inplace=True)

# Concatenate labels with original data
Final_data = pd.concat((data, labels), axis=1)

# Compute mean of quality metrics for each cluster and export
quality_mean = Final_data.groupby(['group']).agg([np.mean])
quality_mean.to_csv(r'D:\MLAP\PRT2\2000kmeanstry.csv')
