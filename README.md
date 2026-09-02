# Retail Demand Intelligence

### Growth • Customer Retention • Statistical Analysis • Demand Forecasting

An end-to-end retail analytics project that combines **MySQL, Python, and Power BI** to analyze business growth, customer retention, statistical relationships, demand patterns, anomalies, and future demand.

---

## Business Problem

Retail businesses need to understand not only how much they sell, but also:

- What is driving revenue growth or decline?
- Are customers returning after their first purchase?
- Does discounting influence purchase quantity?
- Are there meaningful differences between customer groups?
- What demand patterns and seasonality exist?
- Are there unusual demand spikes or drops?
- What level of demand can be expected in the near future?

This project analyzes historical retail transactions to answer these questions and translate the findings into actionable business recommendations.

---

# Project Objectives

1. Measure revenue, transaction, customer, unit, and AOV growth.
2. Analyze customer retention and repeat purchasing behavior.
3. Statistically evaluate relationships between discounts, price, quantity, customer type, and category.
4. Identify demand trends, weekly patterns, and anomalies.
5. Compare multiple forecasting approaches using out-of-sample validation.
6. Translate analytical findings into business and inventory planning recommendations.

---

# Dataset

The project uses the **Retail Transaction Dataset** by Fahad Rehman from Kaggle.

The dataset contains:

- **100,000 transactions**
- **95,215 unique customers**
- **4 product categories**
- **4 payment methods**
- Approximately **one year of transaction history**
- Transaction-level quantity, price, discount, and revenue data

### Main Fields

| Field | Description |
|---|---|
| CustomerID | Customer identifier |
| ProductID | Product identifier |
| Quantity | Units purchased |
| Price | Unit price |
| TransactionDate | Transaction date and time |
| PaymentMethod | Payment method |
| StoreLocation | Store/location information |
| ProductCategory | Product category |
| DiscountApplied(%) | Discount percentage |
| TotalAmount | Transaction revenue |

The original dataset is not redistributed in this repository. See [`data/README.md`](data/README.md) for the source and reproduction instructions.

---

# Analytical Approach

The project follows an end-to-end workflow:

```text
Raw Transaction Data
        ↓
Data Validation & Preparation
        ↓
MySQL Business Analysis
        ↓
Growth & Retention Analysis
        ↓
Statistical Analysis
        ↓
Daily Demand Time Series
        ↓
Anomaly Detection
        ↓
Forecast Model Comparison
        ↓
Power BI Dashboard
        ↓
Business Recommendations
