# ============================================
# 01. TIME SERIES ANALYSIS
# Retail Demand Intelligence
# ============================================

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------
# Load daily demand data
# --------------------------------------------

df = pd.read_csv("data/daily_demand.csv")

df["Demand_Date"] = pd.to_datetime(df["Demand_Date"])

df = df.sort_values("Demand_Date").reset_index(drop=True)


# --------------------------------------------
# Basic time-series validation
# --------------------------------------------

print("Observations:", len(df))
print("Start Date:", df["Demand_Date"].min())
print("End Date:", df["Demand_Date"].max())

print("\nMissing Values:")
print(df.isnull().sum())


# --------------------------------------------
# Remove clearly partial first day
# --------------------------------------------

df_clean = df[
    df["Demand_Date"] > "2023-04-29"
].copy()

df_clean = (
    df_clean
    .sort_values("Demand_Date")
    .reset_index(drop=True)
)


# --------------------------------------------
# Daily revenue summary
# --------------------------------------------

print("\nDaily Revenue Statistics:")
print(df_clean["Revenue"].describe())


# --------------------------------------------
# 7-Day Rolling Revenue
# --------------------------------------------

df_clean["Revenue_7D_MA"] = (
    df_clean["Revenue"]
    .rolling(7)
    .mean()
)

df_clean["Revenue_7D_STD"] = (
    df_clean["Revenue"]
    .rolling(7)
    .std()
)


# --------------------------------------------
# Revenue Volatility
# --------------------------------------------

average_rolling_volatility = (
    df_clean["Revenue_7D_STD"].mean()
)

print(
    "\nAverage 7-Day Revenue Volatility:",
    round(average_rolling_volatility, 2)
)


# --------------------------------------------
# Revenue Trend Visualization
# --------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    df_clean["Demand_Date"],
    df_clean["Revenue"],
    label="Daily Revenue"
)

plt.plot(
    df_clean["Demand_Date"],
    df_clean["Revenue_7D_MA"],
    label="7-Day Moving Average"
)

plt.title("Retail Daily Revenue Trend")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()
plt.tight_layout()
plt.show()


# --------------------------------------------
# Day-of-Week Analysis
# --------------------------------------------

weekday_summary = (
    df_clean
    .assign(
        Day=df_clean["Demand_Date"].dt.day_name()
    )
    .groupby("Day")
    .agg(
        Avg_Revenue=("Revenue", "mean"),
        Avg_Units=("Units", "mean"),
        Avg_Orders=("Orders", "mean")
    )
    .reindex([
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ])
)

print("\nDay-of-Week Demand:")
print(weekday_summary.round(2))
