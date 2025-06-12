"""
This script reads multiple clustered CSV files containing GNSS and signal quality data,
concatenates them into a single DataFrame, and saves the result to a new CSV file.

Steps:
1. Load all CSV files from the input folder.
2. Concatenate them into one DataFrame.
3. Save the merged data to a target CSV file.
"""

import pandas as pd
import glob
import gc
import os

# Path to the folder containing the 45 long-term data CSVs
file_pathr = r"D:\MLAP\PRT2\ClusteredCellular\*.csv"
# Output directory
file_pathw = r'D:\MLAP\PRT2\write'

# Read all CSV file paths from the input folder
csv_listr = glob.glob(file_pathr)

# Initialize an empty DataFrame with expected columns
columns1 = ['latitude', 'longitude', 'signal_quality']
GNSS = pd.DataFrame(columns=columns1, index=None)

# Loop over all CSVs and concatenate them
for i in range(len(csv_listr)):
    with open(csv_listr[i]) as r:
        longterm = pd.read_csv(r)
        GNSS = pd.concat([longterm, GNSS])

# Save the concatenated result
GNSS.to_csv(os.path.join(file_pathw, 'Cellular.csv'), index=None)
