# ============================================
# 04. DEMAND FORECASTING
# Retail Demand Intelligence
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX


# ============================================
# 1. Load and Prepare Data
# ============================================

df = pd.read_csv("data/daily_demand.csv")

df["Demand_Date"] = pd.to_datetime(
    df["Demand_Date"]
)

df = (
    df.sort_values("Demand_Date")
      .reset_index(drop=True)
)

# Remove clearly partial first day
df_clean = df[
    df["Demand_Date"] > "2023-04-29"
].copy()

df_clean = (
    df_clean
    .sort_values("Demand_Date")
    .reset_index(drop=True)
)

# Revenue time series
y = (
    df_clean
    .set_index("Demand_Date")["Revenue"]
)


# ============================================
# 2. Train / Test Split
# ============================================

test_size = 30

train = y.iloc[:-test_size]
test = y.iloc[-test_size:]

print("Training Period:",
      train.index.min(),
      "to",
      train.index.max())

print("Test Period:",
      test.index.min(),
      "to",
      test.index.max())


# ============================================
# 3. Evaluation Function
# ============================================

def evaluate_model(actual, predicted):

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    mape = np.mean(
        np.abs(
            (actual - predicted) / actual
        )
    ) * 100

    return mae, rmse, mape


# ============================================
# 4. Naive Forecast
# ============================================

naive_forecast = pd.Series(
    train.iloc[-1],
    index=test.index
)


# ============================================
# 5. 7-Day Moving Average
# ============================================

ma7_value = train.tail(7).mean()

ma7_forecast = pd.Series(
    ma7_value,
    index=test.index
)


# ============================================
# 6. Exponential Smoothing
# ============================================

exp_model = ExponentialSmoothing(
    train,
    trend=None,
    seasonal=None
).fit()

exp_forecast = exp_model.forecast(
    test_size
)


# ============================================
# 7. Holt-Winters
# ============================================

hw_model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=7
).fit()

hw_forecast = hw_model.forecast(
    test_size
)


# ============================================
# 8. SARIMA
# ============================================

sarima_model = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 7),
    enforce_stationarity=False,
    enforce_invertibility=False
).fit(disp=False)

sarima_forecast = sarima_model.forecast(
    test_size
)


# ============================================
# 9. Model Comparison
# ============================================

models = {
    "Naive": naive_forecast,
    "7-Day Moving Average": ma7_forecast,
    "Exponential Smoothing": exp_forecast,
    "Holt-Winters": hw_forecast,
    "SARIMA": sarima_forecast
}

results = []

for name, forecast in models.items():

    mae, rmse, mape = evaluate_model(
        test,
        forecast
    )

    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE (%)": mape
    })

results_df = pd.DataFrame(results)

results_df = (
    results_df
    .sort_values("MAE")
    .reset_index(drop=True)
)

print("\nModel Comparison")
print(results_df.round(2))


# ============================================
# 10. Rolling Validation
# ============================================

rolling_results = []

window_size = 30

for i in range(3):

    test_end = len(y) - i * window_size
    test_start = test_end - window_size
    train_end = test_start

    train_roll = y.iloc[:train_end]
    test_roll = y.iloc[test_start:test_end]

    # 7-Day Moving Average
    ma7_value = train_roll.tail(7).mean()

    ma7_pred = pd.Series(
        ma7_value,
        index=test_roll.index
    )

    # SARIMA
    sarima_model = SARIMAX(
        train_roll,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 7),
        enforce_stationarity=False,
        enforce_invertibility=False
    ).fit(disp=False)

    sarima_pred = sarima_model.forecast(
        window_size
    )

    for model_name, prediction in [
        ("7-Day Moving Average", ma7_pred),
        ("SARIMA", sarima_pred)
    ]:

        mae, rmse, mape = evaluate_model(
            test_roll,
            prediction
        )

        rolling_results.append({
            "Window": i + 1,
            "Model": model_name,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE (%)": mape
        })


rolling_results_df = pd.DataFrame(
    rolling_results
)

print("\nRolling Validation")
print(
    rolling_results_df.round(2)
)


# ============================================
# 11. Average Rolling Performance
# ============================================

rolling_summary = (
    rolling_results_df
    .groupby("Model")[
        ["MAE", "RMSE", "MAPE (%)"]
    ]
    .mean()
    .sort_values("MAE")
)

print("\nAverage Rolling Validation")
print(
    rolling_summary.round(2)
)


# ============================================
# 12. Final Model: 7-Day Moving Average
# ============================================

last_7_day_average = (
    y.tail(7).mean()
)

print(
    "\nLatest 7-Day Average Daily Revenue:",
    round(last_7_day_average, 2)
)


# ============================================
# 13. 90-Day Future Forecast
# ============================================

future_dates = pd.date_range(
    start=y.index.max()
          + pd.Timedelta(days=1),
    periods=90,
    freq="D"
)

future_forecast = pd.Series(
    last_7_day_average,
    index=future_dates
)


# ============================================
# 14. Forecast Totals
# ============================================

forecast_30 = (
    future_forecast.iloc[:30].sum()
)

forecast_60 = (
    future_forecast.iloc[:60].sum()
)

forecast_90 = (
    future_forecast.iloc[:90].sum()
)

print("\nFuture Revenue Forecast")
print("-----------------------")

print(
    "Next 30 Days:",
    round(forecast_30, 2)
)

print(
    "Next 60 Days:",
    round(forecast_60, 2)
)

print(
    "Next 90 Days:",
    round(forecast_90, 2)
)


# ============================================
# 15. Final Forecast Visualization
# ============================================

plt.figure(figsize=(14, 6))

plt.plot(
    train.index,
    train.values,
    label="Training Revenue"
)

plt.plot(
    test.index,
    test.values,
    label="Actual Test Revenue"
)

plt.plot(
    ma7_forecast.index,
    ma7_forecast.values,
    label="7-Day MA Test Forecast"
)

plt.plot(
    future_forecast.index,
    future_forecast.values,
    label="90-Day Future Forecast"
)

plt.axvline(
    x=test.index[0],
    linestyle="--",
    label="Test Period Start"
)

plt.axvline(
    x=future_forecast.index[0],
    linestyle="--",
    label="Future Forecast Start"
)

plt.title(
    "Retail Revenue Forecast Using 7-Day Moving Average"
)

plt.xlabel("Date")
plt.ylabel("Daily Revenue")

plt.legend()
plt.tight_layout()
plt.show()
