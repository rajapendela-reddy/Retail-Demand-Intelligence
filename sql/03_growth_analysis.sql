USE retail_demand_intelligence;

-- ============================================
-- 03. GROWTH ANALYSIS
-- ============================================

-- Monthly revenue, transactions, customers,
-- units and AOV
WITH monthly_metrics AS (
    SELECT
        Month_Start,
        SUM(TotalAmount) AS Revenue,
        COUNT(*) AS Transactions,
        COUNT(DISTINCT CustomerID) AS Customers,
        SUM(Quantity) AS Units,
        AVG(TotalAmount) AS AOV
    FROM retail_transactions
    GROUP BY Month_Start
)

SELECT
    Month_Start,
    ROUND(Revenue, 2) AS Revenue,
    Transactions,
    Customers,
    Units,
    ROUND(AOV, 2) AS AOV
FROM monthly_metrics
ORDER BY Month_Start;


-- ============================================
-- Month-over-Month Growth
-- ============================================

WITH monthly_metrics AS (
    SELECT
        Month_Start,
        SUM(TotalAmount) AS Revenue,
        COUNT(*) AS Transactions,
        COUNT(DISTINCT CustomerID) AS Customers,
        SUM(Quantity) AS Units,
        AVG(TotalAmount) AS AOV
    FROM retail_transactions
    GROUP BY Month_Start
),

growth_metrics AS (
    SELECT
        *,
        LAG(Revenue) OVER (
            ORDER BY Month_Start
        ) AS Previous_Revenue,

        LAG(Transactions) OVER (
            ORDER BY Month_Start
        ) AS Previous_Transactions,

        LAG(Customers) OVER (
            ORDER BY Month_Start
        ) AS Previous_Customers,

        LAG(Units) OVER (
            ORDER BY Month_Start
        ) AS Previous_Units,

        LAG(AOV) OVER (
            ORDER BY Month_Start
        ) AS Previous_AOV

    FROM monthly_metrics
)

SELECT
    Month_Start,

    ROUND(Revenue, 2) AS Revenue,

    ROUND(
        (Revenue - Previous_Revenue)
        / Previous_Revenue * 100,
        2
    ) AS Revenue_Growth_Pct,

    ROUND(
        (Transactions - Previous_Transactions)
        / Previous_Transactions * 100,
        2
    ) AS Transaction_Growth_Pct,

    ROUND(
        (Customers - Previous_Customers)
        / Previous_Customers * 100,
        2
    ) AS Customer_Growth_Pct,

    ROUND(
        (Units - Previous_Units)
        / Previous_Units * 100,
        2
    ) AS Unit_Growth_Pct,

    ROUND(
        (AOV - Previous_AOV)
        / Previous_AOV * 100,
        2
    ) AS AOV_Growth_Pct

FROM growth_metrics
ORDER BY Month_Start;
