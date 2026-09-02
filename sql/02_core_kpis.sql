USE retail_demand_intelligence;

-- ============================================
-- 02. CORE BUSINESS KPIs
-- ============================================

SELECT
    ROUND(SUM(TotalAmount), 2) AS Total_Revenue,
    COUNT(*) AS Total_Transactions,
    SUM(Quantity) AS Total_Units,
    COUNT(DISTINCT CustomerID) AS Unique_Customers,

    ROUND(AVG(TotalAmount), 2) AS AOV,

    ROUND(
        SUM(Quantity) / COUNT(*),
        2
    ) AS Units_Per_Transaction,

    ROUND(
        COUNT(*) / COUNT(DISTINCT CustomerID),
        2
    ) AS Transactions_Per_Customer

FROM retail_transactions;
