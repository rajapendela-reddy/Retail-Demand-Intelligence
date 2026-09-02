# Retail-Demand-Intelligence
# SQL Analysis

This folder contains the MySQL analysis used in the Retail Demand Intelligence project.

The SQL analysis covers data validation, business KPIs, growth, customer retention, customer behavior, and demand analysis.

## Database

**Database:** `retail_demand_intelligence`

**Main analytical table:** `retail_transactions`

The table contains 100,000 retail transactions covering approximately one year of transaction history.

## SQL Analysis

| File | Purpose |
|---|---|
| `01_data_validation.sql` | Validates transaction volume, date coverage, uniqueness, missing values, and duplicates |
| `02_core_kpis.sql` | Calculates revenue, transactions, units, customers, AOV, and purchase frequency |
| `03_growth_analysis.sql` | Analyzes monthly revenue, transaction, customer, unit, and AOV growth |
| `04_retention_analysis.sql` | Measures one-time vs repeat customers, purchase frequency, and time to second purchase |
| `05_customer_analysis.sql` | Analyzes customer revenue, new vs returning transactions, and category-level repeat behavior |
| `06_demand_analysis.sql` | Creates daily, weekly, and monthly demand summaries for time-series analysis |

## Key SQL Techniques

The project uses:

- Aggregations with `SUM()`, `COUNT()`, and `AVG()`
- `GROUP BY` for customer, category, daily, and monthly analysis
- `CASE` statements for customer and discount segmentation
- `COUNT(DISTINCT ...)` for customer-level metrics
- `LAG()` for month-over-month growth analysis
- `ROW_NUMBER()` for purchase sequencing
- `DATEDIFF()` for customer return timing
- Common Table Expressions (`WITH`) for multi-step analysis
- Conditional aggregation for retention metrics

## Key Findings

### Revenue & Growth

- Total revenue: approximately **$24.83M**
- Total transactions: **100,000**
- February 2024 revenue declined **7.29% MoM**
- The decline was primarily associated with lower transactions, customers, and units.

### Customer Retention

- **95.15%** of customers made only one purchase.
- **4.85%** of customers made multiple purchases.
- Average time to second purchase was approximately **121 days**.

### Category Performance

Revenue was highly balanced across the four categories:

- Books: **25.20%**
- Clothing: **24.99%**
- Electronics: **24.95%**
- Home Decor: **24.86%**

### Demand

Daily and monthly demand summaries created through SQL were used as the foundation for the Python time-series analysis and forecasting.

## SQL → Python Workflow

The SQL workflow prepares and analyzes the transactional data before the forecasting stage:

```text
Raw Transactions
       ↓
Data Validation
       ↓
Business KPIs
       ↓
Growth & Retention Analysis
       ↓
Daily Demand Aggregation
       ↓
Python Time-Series Analysis
       ↓
Forecasting
