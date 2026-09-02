# ============================================
# 03. ANOMALY DETECTION
# Retail Demand Intelligence
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------
# Load daily demand data
# --------------------------------------------

df = pd.read_csv("data/daily_demand.csv")

df["Demand_Date"] = pd.to_datetime(
    df["Demand_Date"]
)

df = (
    df.sort_values("Demand_Date")
      .reset_index(drop=True)
)


# --------------------------------------------
# Remove clearly partial first day
# --------------------------------------------

df = df[
    df["Demand_Date"] > "2023-04-29"
].copy()


# --------------------------------------------
# Calculate 7-Day Rolling Statistics
# --------------------------------------------

df["Rolling_Mean_7D"] = (
    df["Revenue"]
    .rolling(7)
    .mean()
)

df["Rolling_STD_7D"] = (
    df["Revenue"]
    .rolling(7)
    .std()
)


# --------------------------------------------
# Calculate Rolling Z-Score
# --------------------------------------------

df["Z_Score"] = (
    (df["Revenue"] - df["Rolling_Mean_7D"])
    / df["Rolling_STD_7D"]
)


# --------------------------------------------
# Identify Anomalies
# --------------------------------------------

anomalies = df[
    df["Z_Score"].abs() > 2
].copy()


print("Number of anomalies:", len(anomalies))

print("\nDetected Anomalies:")
print(
    anomalies[
        [
            "Demand_Date",
            "Revenue",
            "Rolling_Mean_7D",
            "Z_Score"
        ]
    ].round(2)
)


# --------------------------------------------
# Visualize Anomalies
# --------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    df["Demand_Date"],
    df["Revenue"],
    label="Daily Revenue"
)

plt.scatter(
    anomalies["Demand_Date"],
    anomalies["Revenue"],
    label="Detected Anomaly"
)

plt.title("Retail Revenue Anomaly Detection")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()
plt.tight_layout()
plt.show()
