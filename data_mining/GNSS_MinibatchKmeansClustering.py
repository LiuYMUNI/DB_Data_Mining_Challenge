"""
This script applies MiniBatchKMeans clustering to GNSS (latitude, longitude) data
from multiple preprocessed CSV files. It calculates cluster groupings and average
quality metrics per cluster, then saves the results to separate output files.

Steps:
1. Load each CSV file from the input folder.
2. Perform clustering with MiniBatchKMeans (k=3000, batch size=32768).
3. Append cluster labels to the original data.
4. Compute average values for each cluster group.
5. Save the result to individual CSV files.
"""

import pandas as pd
import time
from joblib import parallel_backend  # For multiprocessing
import numpy as np
import glob  # For automatic file handling
import os
from sklearn.cluster import MiniBatchKMeans  # For clustering

start = time.time()  # Start timing

# Input folder (preprocessed longterm data) and output folder (result)
file_pathr = r"E:\MLA(GROUP WORK)\Data\Longterm_preprocessed\*.csv"
file_pathw = r"E:\MLA(GROUP WORK)\Data\GNSS"

# Get list of input CSV file paths
csv_listr = glob.glob(file_pathr)

# Process each file in the list
for i in range(len(csv_listr)):
    with open(csv_listr[i]) as r:
        data = pd.read_csv(r)  # Load CSV

        # Extract only the latitude and longitude columns
        x = data.iloc[:, :2]

        # Parallel processing context
        with parallel_backend('threading', n_jobs=-1):
            mod = MiniBatchKMeans(n_clusters=3000, batch_size=32768, random_state=42)
            y_pre = mod.fit_predict(x)

    end = time.time()
    print(f"[File {i+1}] run time = {end - start:.2f} seconds")

    # Count points in each cluster
    r1 = pd.Series(mod.labels_).value_counts()

    # Get cluster centers
    r2 = pd.DataFrame(mod.cluster_centers_)

    # Combine center coordinates and cluster counts
    r = pd.concat([r2, r1], axis=1)
    r.columns = ['lat', 'lon', 'n']

    # Assign cluster labels to the original data
    labels = pd.DataFrame(mod.labels_, index=data.index, columns=['group'])
    Final_data = pd.concat([data, labels], axis=1)

    # Calculate mean values per group
    quality_mean = Final_data.groupby(['group']).agg([np.mean])

    # Save to individual CSV file
    output_filename = f"GNSS_minibatch_k=3000_batchsize=32768_file{i+1}.csv"
    quality_mean.to_csv(os.path.join(file_pathw, output_filename), index=None)
