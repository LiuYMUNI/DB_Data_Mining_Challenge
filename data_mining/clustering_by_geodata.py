"""
This script performs KMeans clustering on GPS data (latitude and longitude)
from long-term railway signal data. It then visualizes the clustering result
and calculates cluster centers and counts.

Steps:
1. Load preprocessed signal data (lat/lon/quality).
2. Run KMeans clustering with 2000 clusters.
3. Visualize the cluster results.
4. Compute and save cluster centers and sample counts.
"""

import matplotlib.pyplot as plt
from sklearn.datasets._samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score
import pandas as pd
import time

start = time.time()  # Start timing

# Load cleaned GPS signal data and set 'wagon_ID' as index
data = pd.read_csv(r"C:\Users\82796\OneDrive\桌面\TU\Machine Learning\新建文件夹\longterm2_good_signal.csv", index_col='wagon_ID')

# Drop non-location and non-quality columns
data = data.drop(labels=['timestamp_index', 't_measure', 'time_delta', 't_transfer'], axis=1)

# Extract latitude and longitude columns
x = data.iloc[:, :2]

# KMeans clustering (2000 clusters)
mod = KMeans(n_clusters=2000, random_state=42)
y_pre = mod.fit_predict(x)

end = time.time()  # End timing
print("run time = {}".format(end - start))

# Visualize clustering result
plt.figure(figsize=(20, 8), dpi=80)
plt.scatter(x.iloc[:, 1], x.iloc[:, 0], c=y_pre, s=1)
plt.show()

# Compute number of points per cluster
r1 = pd.Series(mod.labels_).value_counts()

# Get cluster centers
r2 = pd.DataFrame(mod.cluster_centers_)

# Concatenate cluster centers with counts
r = pd.concat([r2, r1], axis=1)
r.columns = ['lat', 'lon', 'n']

# To be continued: attach cluster labels to all data points
