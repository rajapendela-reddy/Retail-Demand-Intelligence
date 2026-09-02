USE retail_demand_intelligence;

-- ============================================
-- 06. DEMAND & TIME-SERIES PREPARATION
-- ============================================


-- ============================================
-- 1. Daily Demand Summary
-- ============================================

SELECT
    DATE(Transaction_Date) AS Demand_Date,

    COUNT(*) AS Orders,

    COUNT(DISTINCT CustomerID) AS Customers,

    SUM(Quantity) AS Units,

    ROUND(SUM(TotalAmount), 2) AS Revenue,

    ROUND(AVG(TotalAmount), 2) AS AOV

FROM retail_transactions

GROUP BY DATE(Transaction_Date)

ORDER BY Demand_Date;


-- ============================================
-- 2. Day-of-Week Demand Pattern
-- ============================================

SELECT
    Day_of_Week,

    COUNT(DISTINCT DATE(Transaction_Date)) AS Days,

    ROUND(
        SUM(TotalAmount) /
        COUNT(DISTINCT DATE(Transaction_Date)),
        2
    ) AS Avg_Daily_Revenue,

    ROUND(
        SUM(Quantity) /
        COUNT(DISTINCT DATE(Transaction_Date)),
        2
    ) AS Avg_Daily_Units,

    ROUND(
        COUNT(*) /
        COUNT(DISTINCT DATE(Transaction_Date)),
        2
    ) AS Avg_Daily_Transactions

FROM retail_transactions

GROUP BY Day_of_Week

ORDER BY
    CASE Day_of_Week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;


-- ============================================
-- 3. Monthly Demand Summary
-- ============================================

SELECT
    Month_Start,

    COUNT(*) AS Transactions,

    COUNT(DISTINCT CustomerID) AS Customers,

    SUM(Quantity) AS Units,

    ROUND(SUM(TotalAmount), 2) AS Revenue,

    ROUND(AVG(TotalAmount), 2) AS AOV

FROM retail_transactions

GROUP BY Month_Start

ORDER BY Month_Start;
