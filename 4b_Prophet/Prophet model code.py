#2. THE PROPHET MODEL (The Good Forecasting Model)



!pip install prophet

from prophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Aggregate data by month
monthly_data = data.groupby('transaction_month')['total_quantity'].sum()

# Create complete monthly date range
full_date_range = pd.date_range(start=monthly_data.index.min(), end=monthly_data.index.max(), freq='MS')
monthly_data = monthly_data.reindex(full_date_range, fill_value=0)
monthly_data.index.freq = 'MS'

# Convert to DataFrame for Prophet
df = monthly_data.reset_index()
df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])

# Train-test split
train_size = int(len(df) * 0.8)
train_df = df[:train_size]
test_df = df[train_size:]

# Prophet model
prophet_model = Prophet(
    changepoint_prior_scale=0.1,
    yearly_seasonality=True,
    seasonality_prior_scale=1,
    seasonality_mode='multiplicative'  # Change to 'additive' if necessary
)
prophet_model.fit(train_df)

# Future predictions (testing period)
future = prophet_model.make_future_dataframe(periods=len(test_df), freq='MS')
forecast = prophet_model.predict(future)

# Extract test forecast
forecast_test = forecast.iloc[train_size:]['yhat']

# Evaluate MAPE
mape = mean_absolute_percentage_error(test_df['y'], forecast_test)
print(f"✅ Prophet MAPE: {mape:.2%}")

# Plot training, test, and Prophet forecast
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(train_df['ds'], train_df['y'], label='Training Data', color='blue')
ax.plot(test_df['ds'], test_df['y'], label='Test Data', color='green')
ax.plot(test_df['ds'], forecast_test, label='Prophet Model', color='red', linestyle='--')
ax.set_title("Prophet Model", fontsize=14)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Total Quantity", fontsize=12)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)
plt.show()

# Extend future predictions by 6 months AFTER the test period
future_extended = prophet_model.make_future_dataframe(periods=len(test_df) + 6, freq='MS')
forecast_extended = prophet_model.predict(future_extended)

# Fix negative predictions
forecast_extended['yhat'] = forecast_extended['yhat'].clip(lower=0)

# Extract ONLY the actual future forecast (AFTER test period)
next_year_forecast = forecast_extended.iloc[len(future):][['ds', 'yhat']]

print("Future Predictions using Prophet Model")
print(next_year_forecast)

# Plot future forecast
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_data.index, monthly_data, label="Original Data", color='blue')
ax.plot(next_year_forecast['ds'], next_year_forecast['yhat'], label='Future Forecast', color='purple')
ax.set_title("Future Forecast using Prophet Model", fontsize=14)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Total Quantity", fontsize=12)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)
plt.show()


# Prediction forecast can be adjusted
# Since dataset was too small, future predictions by Prophet model only predicted upto 6 months
