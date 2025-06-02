# 💉 Vaccine Data Analysis & Forecasting

---

## 🎯 Objectives

* Analyze historical vaccine supply and usage trends
* Compare performance of multiple forecasting models
* Predict future vaccine demand for effective planning

---

## 🗂️ Dataset

* 📆 **Time Range**: September 2021 – November 2024
* 🌍 **Granularity**: Province > District > Tehsil
* 🧾 **Format**: Monthly totals (`transaction_month` in DD/MM/YY)
* 🔢 **Values**: Total quantity of vaccines supplied and used

---

## 🧹 Data Preprocessing

* ✅ Date formatting & sorting
* 🔁 Aggregation at multiple administrative levels
* 📉 Log transformation for variance stabilization
* 📊 Stationarity check using ADF test

---

## 🔮 Models Used

### ⚙️ SARIMA (Seasonal ARIMA)

* 📌 Quarterly seasonality (`m=3`)
* 🧪 AutoARIMA for hyperparameter tuning
* 📈 Rolling forecast with **MAPE: 39.40%**
* ✅ Best suited for stable seasonal patterns

### 🧙 Prophet (by Meta)

* 🌀 Multiplicative seasonality
* 🕐 Handles irregular time intervals well
* 📉 **MAPE: 15.71%**
* 🔎 Strong performance but under SARIMA in long-term projections

### 🤖 XGBoost

* 🧠 Tree-based regressor with engineered features (month, lag, etc.)
* 🔁 Captured complex non-linear trends
* 📉 **MAPE: 4.91%**
* 🚀 Outperformed all models in accuracy, especially short-term forecasting

---

## 📊 Results

* **XGBoost** achieved the lowest MAPE (4.91%) and best overall performance
* **Prophet** balanced performance and flexibility with 15.71% MAPE
* **SARIMA** showed consistent trends with clear seasonality but higher error
* Forecasts highlighted peak usage periods and anticipated supply-demand gaps in 2025

---

## 🧾 Conclusion

This analysis highlights the strength of combining classical and machine learning models for public health forecasting. With accurate demand prediction, healthcare systems can reduce stockouts, allocate resources effectively, and improve vaccine coverage strategies.

---

## 👥 Contributors

* **Zahra Batool**
* **Manahil Mughal**
