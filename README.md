# 💉 Vaccine Data Analysis & Forecasting


## 🎯 Objectives

* Analyze historical vaccine supply and usage trends
* Compare performance of multiple forecasting models
* Predict future vaccine demand for effective planning


## 🗂️ Dataset

* 📆 **Time Range**: September 2021 – November 2024
* 🌍 **Granularity**: Province > District > Tehsil
* 🧾 **Format**: Monthly totals (`transaction_month` in DD/MM/YY)
* 🔢 **Values**: Total quantity of vaccines supplied and used


## 🧹 Data Preprocessing

* ✅ Date formatting & sorting
* 🔁 Aggregation at multiple administrative levels
* 📉 Log transformation for variance stabilization
* 📊 Stationarity check using ADF test


## 🔮 Models Used

### ⚙️ 1. **SARIMA (Seasonal ARIMA) Model – The Reasonable Forecasting Model**

SARIMA (Seasonal AutoRegressive Integrated Moving Average) was selected due to observed **quarterly seasonality** in vaccine distribution.

#### 🔧 Key Features:

* Log transformation and differencing applied for stationarity.
* `auto_arima()` used with **seasonal order `m=3`** (quarterly pattern).
* Rolling forecast strategy used for stable performance evaluation.
* Final model used to forecast **12 months ahead**.

#### 📈 Performance:

* ✅ **MAPE**: **39.40%**
* **Strength**: Strong at capturing repeating seasonal cycles.
* **Limitation**: Assumes linear and stationary relationships; less accurate on non-linear patterns.

### 🧙 2. **Prophet Model – The Good Forecasting Model**

Prophet is built for time series forecasting with strong seasonal and trend components.

#### 🔧 Key Features:

* Multiplicative seasonality mode used.
* Built-in changepoint detection to model trend shifts.
* 6-month future forecasting.
* Negative forecasts clipped to zero to maintain realism.

#### 📈 Performance:

* ✅ **MAPE**: **15.71%**
* **Strength**: Highly interpretable and easy to configure.
* **Limitation**: Performance drops when data is limited or lacks full seasonal cycles.

### 🤖 3. **XGBoost Model – The Best Forecasting Model**

XGBoost is a gradient boosting machine that excels at learning complex, non-linear relationships.

#### 🔧 Feature Engineering:

* **Lag Features**: `lag_1`, `lag_2`, `lag_3`
* **Rolling Mean**: 3-month average
* **Date Encodings**: month, year, sin/cos transformations
* **Decomposition**: trend, seasonal, and differenced values extracted

#### 🧠 Future Forecasting Strategy:

* Iterative forecast updating lag and rolling values per month.
* Trend and seasonality extrapolated using recent patterns.

#### 📈 Performance:

* ✅ **MAPE**: **4.91%**
* **Strength**: Captures non-linear dependencies and interactions.
* **Limitation**: Less interpretable; requires feature engineering and simulation logic.


## 📊 Results

* **SARIMA** was reasonable for modeling seasonal behavior but showed high error due to linear assumptions.
* **Prophet** handled trend changes and multiplicative seasonality better.
* **XGBoost** achieved the lowest MAPE (4.91%) and best overall performance, significantly outperforming both with rich features and low forecast error.
* Forecasts highlighted peak usage periods and anticipated supply-demand gaps in 2025.


## 🧾 Conclusion

This analysis highlights the strength of combining classical and machine learning models for public health forecasting. With accurate demand prediction, healthcare systems can reduce stockouts, allocate resources effectively, and improve vaccine coverage strategies.


## 👥 Contributors

* **Zahra Batool**
* **Manahil Mughal**
