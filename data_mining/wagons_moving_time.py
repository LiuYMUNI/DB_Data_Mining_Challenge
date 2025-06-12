"""
This script analyzes long-term wagon data to calculate the average daily moving time 
for wagons of different types. It processes multiple CSVs, merges them with wagon type 
information, filters invalid timestamps, and calculates per-type moving time statistics.

Steps:
1. Load wagon type mapping.
2. Iterate over each long-term data CSV file.
3. Merge data with type mapping.
4. Filter rows with valid movement timestamps.
5. For each wagon type (1–8), compute:
   - Moving count
   - Number of wagons
   - Moving events per wagon
   - Estimated average moving time per day
6. Append results to CSV.
"""

import pandas as pd
import glob
import gc

# Paths
file_path = r"D:\MLAP\PRT2\Test\*.csv"  # Folder containing the 45 long-term data CSVs
csv_list = glob.glob(file_path)
wagon_type_file = r"D:\MLAP\PRT2\Mapping\211202_wagon_type_mapping.csv"

# Load wagon type mapping (drop duplicates to ensure unique mapping)
with open(wagon_type_file) as f:
    wagon_type_mapping = pd.read_csv(f).drop_duplicates(['wagon_ID'])

# Process each long-term file
for i in range(len(csv_list)):
    with open(csv_list[i]) as f:
        lonterm_01 = pd.read_csv(f)

    # Merge with wagon type info
    merged_data = pd.merge(lonterm_01, wagon_type_mapping, on="wagon_ID")
    merged_data.to_csv('merged_data.csv', mode='a', index=False, header=(i == 0))  # Write header only for the first file

    # Filter out rows with invalid timestamp
    merged_data_withoutNaT = merged_data[~merged_data['timestamp_measure_movement_state'].isin(['NaT'])]

    a_1 = []
    # Analyze movement by wagon type (1–8)
    for t in range(1, 9):
        merged_data_pure = merged_data_withoutNaT[merged_data['wagon_type'] == t]

        # Count 'moving' states
        moving_number_type = merged_data_pure['movement_state'].to_list().count('moving')
        # Count unique wagons
        wagon_total_number_type = merged_data_pure['wagon_ID'].nunique()
        # Avoid division by zero
        if wagon_total_number_type > 0:
            movingnumber_per_wagon_type = moving_number_type / wagon_total_number_type
            moving_time_per_wagon_type = movingnumber_per_wagon_type * 10 / 60 / 24  # Convert to days
        else:
            moving_time_per_wagon_type = 0.0

        a_1.append(moving_time_per_wagon_type)

    print(a_1)
    df_data = pd.DataFrame([a_1])
    df_data.to_csv('year_change.csv', mode='a', header=False, index=False)

    # Clean up memory
    del lonterm_01, merged_data, merged_data_withoutNaT
    del moving_number_type, wagon_total_number_type, movingnumber_per_wagon_type
    del moving_time_per_wagon_type
    gc.collect()
