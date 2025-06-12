"""
This script filters and processes a TUDA dataset to assess GNSS signal quality
based on timestamp delays. The signal quality is mapped to a 0–256 scale based on
latency between position measurement, transfer, and reception.

Steps:
1. Load and filter data where position was determined by cellular data.
2. Remove unnecessary columns.
3. Extract days and time from timestamp strings.
4. Calculate time differences between measurement and transfer timestamps.
5. Identify samples with <30s delay as "good signal".
6. Compute signal quality based on delay between transfer and reception.
7. Export the "good signal" dataset to CSV.
"""

import pandas as pd
from datetime import datetime
import time

start = time.time()  # Start timing

# Load dataset indexed by 'wagon_ID'
table = pd.read_csv(r"D:\MLAP\PRT2\Test\35_211203_TUDA_data.csv", index_col='wagon_ID')

# Filter only cellular-positioned entries
table = table[table['determination_position'].isin([4])]

# Drop unnecessary columns
table = table.drop(labels=[
    'loading_state', 'loading_state_update', 'altitude',
    'signal_quality_satellite', 'signal_quality_hdop', 'determination_position',
    'GNSS_velocity', 'movement_state', 'timestamp_measure_movement_state', 'provider'
], axis=1)

# Extract day and hour from timestamp columns
def transdayhour(df, position, day, hour):
    df.loc[:, 'Timestamp_measure'] = df[position].str.split(' days ')
    p = [df.loc[:, 'Timestamp_measure'].values[x][0] for x in range(len(df))]
    df.loc[:, day] = p
    p = [df.loc[:, 'Timestamp_measure'].values[x][1] for x in range(len(df))]
    df.loc[:, hour] = p
    return df

transdayhour(table, 'timestamp_measure_position', 'Timestamp_measure_position_day', 'Timestamp_measure_position_hour')
transdayhour(table, 'timestamp_transfer', 'Timestamp_measure_transfer_day', 'Timestamp_measure_transfer_hour')

# Convert day strings to integers
def str_num_to_int(df, time_day):
    data_int = list(map(int, map(eval, df[time_day].values)))
    df.loc[:, time_day] = data_int
    return df

str_num_to_int(table, 'Timestamp_measure_position_day')
str_num_to_int(table, 'Timestamp_measure_transfer_day')

# Compute day and hour difference between measurement and transfer
def timediff(df):
    df.loc[:, 'day_diff'] = df['Timestamp_measure_transfer_day'] - df['Timestamp_measure_position_day']
    df.loc[:, 'hour_diff'] = pd.to_datetime(df['Timestamp_measure_transfer_hour']) - pd.to_datetime(df['Timestamp_measure_position_hour'])
    return df

timediff(table)

# Define 30s and 0s timedelta for thresholding
delta_30s = datetime(2000, 7, 14, 8, 15, 30) - datetime(2000, 7, 14, 8, 15, 0)
delta_0s = datetime(2000, 7, 14, 8, 15, 0) - datetime(2000, 7, 14, 8, 15, 0)

# Identify good and bad signal samples
table_goodsignal = table[(table['hour_diff'] <= delta_30s) & (table['hour_diff'] >= delta_0s) & (table['day_diff'] == 0)]
table_nosignal = table[(table['day_diff'] != 0) | (table['hour_diff'] > delta_30s) | (table['hour_diff'] < delta_0s)]

# Further split timestamp_index into day and hour
transdayhour(table_goodsignal, 'timestamp_index', 'Timestamp_receive_day', 'Timestamp_receive_hour')
str_num_to_int(table_goodsignal, 'Timestamp_receive_day')

# Compute time difference between transfer and receive timestamps
def timediff_receive(df):
    df.loc[:, 'day_diff_receive'] = df['Timestamp_receive_day'] - df['Timestamp_measure_transfer_day']
    df.loc[:, 'hour_diff_receive'] = pd.to_datetime(df['Timestamp_receive_hour']) - pd.to_datetime(df['Timestamp_measure_transfer_hour'])
    return df

timediff_receive(table_goodsignal)

# Map delay to signal quality (0 = 30s, 256 = 0s)
table_goodsignal.loc[:, 'signal_quality'] = (1 - table_goodsignal['hour_diff_receive'] / delta_30s) * 256

# Export good signal samples
table_goodsignal.to_csv('goodsignal.csv', mode='a')

end = time.time()  # End timing
print("run time = {}".format(end - start))
