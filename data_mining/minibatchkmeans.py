"""
This script demonstrates the use of MiniBatchKMeans clustering on synthetic 2D data.
It visualizes both the raw data distribution and the clustering result.

Steps:
1. Generate synthetic data with `make_blobs`.
2. Apply MiniBatchKMeans clustering (k=5).
3. Visualize before and after clustering using matplotlib.
"""

import time
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import MiniBatchKMeans
from sklearn.datasets import make_blobs

# Enable Chinese font support (if needed) and proper minus symbol display
matplotlib.rcParams['font.sans-serif'] = [u'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# Generate synthetic data (1000 samples, 2 features, 5 clusters)
k = 5
X, Y = make_blobs(n_samples=1000, n_features=2, centers=k, random_state=1)

# Cluster using MiniBatchKMeans
s = time.time()
km = MiniBatchKMeans(n_clusters=k, batch_size=100)
km.fit(X)
print("Clustering time using MiniBatchKMeans:", time.time() - s)

# Get clustering results
label_pred = km.labels_          # Cluster labels for each point
centroids = km.cluster_centers_  # Coordinates of cluster centers

# Plot raw data (before clustering)
plt.subplot(121)
plt.scatter(X[:, 0], X[:, 1], s=50)
plt.title("Raw Data Distribution")
plt.subplots_adjust(wspace=0.5)

# Plot clustering results
plt.subplot(122)
plt.scatter(X[:, 0], X[:, 1], c=label_pred, s=50, cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='o', s=100)
plt.title("MiniBatchKMeans Clustering Result")
plt.show()
