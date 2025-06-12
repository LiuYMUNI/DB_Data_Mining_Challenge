"""
Feature Engineering for Delay Analysis in Railway Operations.

This script processes a dataset of operational and environmental features from 
railway networks (e.g., Maschen node) and generates additional features that 
capture delay risk, operational efficiency, and potential disruption signals.

Assumes input data contains the following columns:
- avg_speed
- track_utilization
- weather_risk
- signal_quality
- maintenance_flag
- station_congestion
- num_switches

Output:
- Adds 6 new engineered features to the DataFrame:
    1. delay_score: Weighted risk indicator for expected delays.
    2. efficiency_index: Speed adjusted by infrastructure complexity.
    3. congestion_pressure: Joint impact of track and station load.
    4. signal_speed_mismatch: Deviation between expected and actual signal-speed correlation.
    5. composite_risk: Summed risk factors contributing to disruption.
    6. disruption_flag: Binary indicator for likely service disruptions.
"""

import pandas as pd
import numpy as np

X = pd.read_csv(r"E:\sid\TU Darmstadt\Module und Lehrveranstaltungen\WS2022\MLA practical\Maschen_data.csv")

# Feature 1: Delay likelihood score (rule-based weighted sum)
X["delay_score"] = (
    0.3 * (1 - X["signal_quality"]) +
    0.2 * X["track_utilization"] +
    0.2 * X["station_congestion"] +
    0.1 * X["weather_risk"] +
    0.2 * X["maintenance_flag"]
)

# Feature 2: Efficiency indicator (speed normalized by switch complexity and congestion)
X["efficiency_index"] = X["avg_speed"] / (1 + X["num_switches"] * X["station_congestion"])

# Feature 3: Congestion-pressure interaction
X["congestion_pressure"] = X["track_utilization"] * X["station_congestion"]

# Feature 4: Signal-speed mismatch (ideally high speed should pair with high signal quality)
X["signal_speed_mismatch"] = np.abs(X["signal_quality"] - X["avg_speed"] / 120.0)  # Assuming 120 km/h expected speed

# Feature 5: Composite risk index
X["composite_risk"] = (
    X["weather_risk"] +
    X["maintenance_flag"] +
    (1 - X["signal_quality"]) +
    X["station_congestion"]
)

# Feature 6: Binary flag for likely disruption
X["disruption_flag"] = (
    (X["signal_quality"] < 0.6) |
    (X["weather_risk"] >= 2) |
    (X["station_congestion"] > 0.9) |
    (X["maintenance_flag"] == 1)
).astype(int)
# Save the updated DataFrame with new features to engineered_features.csv
X.to_csv(r"E:\sid\TU Darmstadt\Module und Lehrveranstaltungen\WS2022\MLA practical\engineered_features.csv", index=True)
