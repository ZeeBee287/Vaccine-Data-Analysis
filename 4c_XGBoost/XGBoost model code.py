#3. XGBoost MODEL (The Good Forecasting Model)



#!pip install --upgrade scikit-learn xgboost
!pip install scikit-learn==1.2.2 xgboost==1.7.6

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_percentage_error

# Feature Engineering Function
def feature_engineering(data):
    data['lag_1'] = data['total_quantity'].shift(1)
    data['lag_2'] = data['total_quantity'].shift(2)
    data['lag_3'] = data['total_quantity'].shift(3)
    data['rolling_mean_3'] = data['total_quantity'].rolling(window=3).mean()
    data['month'] = data['transaction_month'].dt.month
    data['year'] = data['transaction_month'].dt.year
    data['month_year'] = data['month'] * data['year']  # Interaction term
    data['month_sin'] = np.sin(2 * np.pi * data['month'] / 3)  # Seasonal component
    data['month_cos'] = np.cos(2 * np.pi * data['month'] / 3)  # Seasonal component
    data = data.dropna()  # Drop rows with NaN after feature creation
    return data

# Preprocessing and Feature Engineering
monthly_data = data.groupby('transaction_month')['total_quantity'].sum().reset_index()
monthly_data['month_index'] = (monthly_data['transaction_month'] - monthly_data['transaction_month'].min()).dt.days
monthly_data = feature_engineering(monthly_data)

# Decompose the time series to extract trend and seasonality
result = seasonal_decompose(monthly_data['total_quantity'], model='additive', period=3)
monthly_data['trend'] = result.trend
monthly_data['seasonal'] = result.seasonal
monthly_data['diff'] = monthly_data['total_quantity'].diff()
monthly_data = monthly_data.dropna()

# Split data (80% train, 20% test)
train_size = int(len(monthly_data) * 0.8)
train_data = monthly_data.iloc[:train_size]
test_data = monthly_data.iloc[train_size:]

# Define features and target for training/testing
features = ['month_index', 'lag_1', 'lag_2', 'lag_3', 'rolling_mean_3', 'month', 'year',
            'month_year', 'month_sin', 'month_cos', 'trend', 'seasonal', 'diff']

X_train = train_data[features]
y_train = train_data['total_quantity']

X_test = test_data[features]
y_test = test_data['total_quantity']

# Initialize XGBoost Model
xgb_model = XGBRegressor(objective='reg:squarederror',
                          random_state=42,
                          learning_rate=0.01,
                          n_estimators=105,
                          max_depth=8,
                          subsample=0.7,
                          colsample_bytree=1)

# Train the XGBoost Model
xgb_model.fit(X_train, y_train)

# Make Predictions
y_pred = xgb_model.predict(X_test)

# Evaluate Model Performance
mape = mean_absolute_percentage_error(y_test, y_pred) * 100
print(f"✅ XGBoost MAPE: {mape:.2f}%")

# Plot results
plt.figure(figsize=(12, 6))

# Training Data
plt.plot(train_data['transaction_month'], train_data['total_quantity'], label="Training Data", color='blue')

# Test Data
plt.plot(test_data['transaction_month'], y_test, label="Test Data", color='green')

# Forecasted Data
plt.plot(test_data['transaction_month'], y_pred, label="XGBoost Model", color='red', linestyle="--")

plt.xlabel("Month")
plt.ylabel("Total Quantity")
plt.title("XGBoost Model")
plt.legend()
plt.grid()
plt.show()

# Future Forecasting (12 months ahead)
future_steps = 12
future_dates = pd.date_range(start=monthly_data['transaction_month'].max() + pd.DateOffset(months=1),
                             periods=future_steps, freq='MS')

future_data = pd.DataFrame({'transaction_month': future_dates})
future_data['month_index'] = (future_data['transaction_month'] - monthly_data['transaction_month'].min()).dt.days
future_data['month'] = future_data['transaction_month'].dt.month
future_data['year'] = future_data['transaction_month'].dt.year
future_data['month_year'] = future_data['month'] * future_data['year']
future_data['month_sin'] = np.sin(2 * np.pi * future_data['month'] / 3)
future_data['month_cos'] = np.cos(2 * np.pi * future_data['month'] / 3)

# Use Moving Averages to extrapolate trend & seasonality
future_data['trend'] = monthly_data['trend'].rolling(window=3).mean().iloc[-1]
future_data['seasonal'] = monthly_data['seasonal'].rolling(window=3).mean().iloc[-1]

# Initialize list to store future predictions
future_forecast = []
prev_values = list(monthly_data['total_quantity'].iloc[-3:])  # Last 3 known values

for i in range(future_steps):
    row = future_data.iloc[i].copy()
    
    # Dynamically update lag features
    row['lag_1'], row['lag_2'], row['lag_3'] = prev_values[-1], prev_values[-2], prev_values[-3]
    row['rolling_mean_3'] = np.mean(prev_values)  # Rolling mean of last 3 values
    row['diff'] = prev_values[-1] - prev_values[-2]  # Difference between last two values

    # Predict next step
    pred = xgb_model.predict(row[features].values.reshape(1, -1))[0]
    future_forecast.append(pred)

    # Update previous values for the next step
    prev_values.append(pred)
    prev_values.pop(0)  # Keep only the last 3 values

future_forecast = np.array(future_forecast)


# Plot Future Forecast
plt.figure(figsize=(12, 6))
plt.plot(monthly_data['transaction_month'], monthly_data['total_quantity'], label="Original Data", color='blue')
plt.plot(future_dates, future_forecast, label="Future Forecast", color='purple')

plt.xlabel("Month")
plt.ylabel("Total Quantity")
plt.title("Future Forecast using XGBoost")
plt.legend()
plt.grid()
plt.show()
