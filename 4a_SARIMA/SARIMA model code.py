#1. SARIMA MODEL (The Reasonable Forecasting Model)



!pip install pmdarima

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Load and preprocess data
monthly_data = data.groupby('transaction_month')['total_quantity'].sum()
monthly_data.index = pd.to_datetime(monthly_data.index)
monthly_data = monthly_data.asfreq('MS').fillna(0)

# Log transformation
monthly_data_log = np.log1p(monthly_data)

# Stationarity check and differencing (forcing at least one differencing step)
def make_stationary(series):
    p_value = adfuller(series)[1]
    if p_value > 0.05:
        return series.diff().dropna()  # Force differencing if needed
    return series

# Apply differencing
monthly_data_log = make_stationary(monthly_data_log)

# Train-test split (80/20)
train_size = int(len(monthly_data_log) * 0.8)
train_data, test_data = monthly_data_log[:train_size], monthly_data_log[train_size:]

# Find best SARIMA order with m=3 (quarterly cycles)
best_arima = auto_arima(train_data, seasonal=True, m=3,
                        stepwise=True, trace=True, suppress_warnings=True,
                        max_p=5, max_d=1, max_q=5,
                        max_P=2, max_D=1, max_Q=2,
                        enforce_stationarity=False, enforce_invertibility=False,
                        test='kpss', seasonal_test='ocsb')

best_order = best_arima.order
best_seasonal_order = best_arima.seasonal_order

print(f"✅ Optimal SARIMA Order: {best_order}")
print(f"✅ Optimal Seasonal Order: {best_seasonal_order}")

# Fit SARIMA model
final_model = SARIMAX(train_data, order=best_order, seasonal_order=best_seasonal_order,
                      enforce_stationarity=False, enforce_invertibility=False).fit()

# Rolling Forecasting (Smarter Rolling Forecast)
rolling_predictions = []
history = list(train_data)
for t in range(len(test_data)):
    model = SARIMAX(history, order=best_order, seasonal_order=best_seasonal_order,
                    enforce_stationarity=False, enforce_invertibility=False).fit()
    forecast_log = model.forecast(steps=1)
    rolling_predictions.append(forecast_log[0])
    history.append(test_data.iloc[t])

# Convert back from log scale
forecast = np.expm1(rolling_predictions)
forecast = np.maximum(forecast, 0)  # Ensure no negative values

# Convert test data back
test_data_original = np.expm1(test_data)

# Calculate MAPE
mape = np.mean(np.abs((test_data_original - forecast) / (test_data_original + 1e-9))) * 100
print(f"✅ SARIMA MAPE: {mape:.2f}%")

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(train_data.index, np.expm1(train_data), label="Training Data", color='blue')
plt.plot(test_data.index, test_data_original, label="Test Data", color='green')
plt.plot(test_data.index, forecast, label="SARIMA Model", color='red', linestyle="--")

plt.xlabel("Month")
plt.ylabel("Total Quantity")
plt.title("SARIMA Model")
plt.legend()
plt.grid()
plt.show()

# Future Forecasting
forecast_horizon = 12
future_forecast_log = final_model.forecast(steps=forecast_horizon)
future_forecast = np.expm1(future_forecast_log)
future_forecast = np.maximum(future_forecast, 0)

future_dates = pd.date_range(start=monthly_data.index[-1] + pd.DateOffset(months=1),
                             periods=forecast_horizon, freq='MS')

# Plot future predictions
plt.figure(figsize=(12, 6))
plt.plot(monthly_data.index, monthly_data, label="Original Data", color='blue')
plt.plot(future_dates, future_forecast, label="Future Forecast", color='purple')

plt.xlabel("Month")
plt.ylabel("Total Quantity")
plt.title("Future Forecast using SARIMA")
plt.legend()
plt.grid()
plt.show()
