USE retail_demand_intelligence;

-- ============================================
-- 05. CUSTOMER ANALYSIS
-- ============================================


-- ============================================
-- 1. Customer Purchase Frequency & Revenue
-- ============================================

SELECT
    CustomerID,
    COUNT(*) AS Purchase_Count,
    SUM(Quantity) AS Total_Units,
    ROUND(SUM(TotalAmount), 2) AS Total_Revenue,
    ROUND(AVG(TotalAmount), 2) AS Customer_AOV
FROM retail_transactions
GROUP BY CustomerID
ORDER BY Total_Revenue DESC;


-- ============================================
-- 2. New vs Returning Transaction Analysis
-- ============================================

WITH ranked_transactions AS (
    SELECT
        CustomerID,
        Transaction_Date,
        TotalAmount,

        ROW_NUMBER() OVER (
            PARTITION BY CustomerID
            ORDER BY Transaction_Date
        ) AS Purchase_Number

    FROM retail_transactions
)

SELECT
    CASE
        WHEN Purchase_Number = 1
        THEN 'New Customer'
        ELSE 'Returning Customer'
    END AS Customer_Type,

    COUNT(*) AS Transactions,

    ROUND(SUM(TotalAmount), 2) AS Revenue,

    ROUND(AVG(TotalAmount), 2) AS AOV

FROM ranked_transactions

GROUP BY
    CASE
        WHEN Purchase_Number = 1
        THEN 'New Customer'
        ELSE 'Returning Customer'
    END

ORDER BY Revenue DESC;


-- ============================================
-- 3. Category-Level Repeat Purchase Rate
-- ============================================

WITH ranked_transactions AS (
    SELECT
        CustomerID,
        ProductCategory,
        Transaction_Date,

        ROW_NUMBER() OVER (
            PARTITION BY CustomerID
            ORDER BY Transaction_Date
        ) AS Purchase_Number

    FROM retail_transactions
)

SELECT
    ProductCategory,

    COUNT(DISTINCT CustomerID) AS Customers,

    COUNT(
        DISTINCT CASE
            WHEN Purchase_Number > 1
            THEN CustomerID
        END
    ) AS Repeat_Customers,

    ROUND(
        COUNT(
            DISTINCT CASE
                WHEN Purchase_Number > 1
                THEN CustomerID
            END
        )
        / COUNT(DISTINCT CustomerID) * 100,
        2
    ) AS Repeat_Customer_Pct

FROM ranked_transactions

GROUP BY ProductCategory

ORDER BY Repeat_Customer_Pct DESC;
