USE retail_demand_intelligence;

-- ============================================
-- 04. CUSTOMER RETENTION ANALYSIS
-- ============================================

-- ============================================
-- 1. One-Time vs Repeat Customers
-- ============================================

SELECT
    COUNT(*) AS Total_Customers,

    SUM(
        CASE
            WHEN Purchase_Count = 1 THEN 1
            ELSE 0
        END
    ) AS One_Time_Customers,

    SUM(
        CASE
            WHEN Purchase_Count > 1 THEN 1
            ELSE 0
        END
    ) AS Repeat_Customers,

    ROUND(
        SUM(
            CASE
                WHEN Purchase_Count = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*) * 100,
        2
    ) AS One_Time_Customer_Pct,

    ROUND(
        SUM(
            CASE
                WHEN Purchase_Count > 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*) * 100,
        2
    ) AS Repeat_Customer_Pct

FROM
(
    SELECT
        CustomerID,
        COUNT(*) AS Purchase_Count
    FROM retail_transactions
    GROUP BY CustomerID
) customer_summary;


-- ============================================
-- 2. Purchase Frequency Distribution
-- ============================================

SELECT
    Purchase_Count,
    COUNT(*) AS Customers,

    ROUND(
        COUNT(*) /
        (SELECT COUNT(DISTINCT CustomerID)
         FROM retail_transactions) * 100,
        2
    ) AS Customer_Pct

FROM
(
    SELECT
        CustomerID,
        COUNT(*) AS Purchase_Count
    FROM retail_transactions
    GROUP BY CustomerID
) customer_summary

GROUP BY Purchase_Count
ORDER BY Purchase_Count;


-- ============================================
-- 3. Average Days to Second Purchase
-- ============================================

WITH ranked_purchases AS (
    SELECT
        CustomerID,
        Transaction_Date,

        ROW_NUMBER() OVER (
            PARTITION BY CustomerID
            ORDER BY Transaction_Date
        ) AS Purchase_Number

    FROM retail_transactions
),

first_second_purchase AS (
    SELECT
        CustomerID,

        MAX(
            CASE
                WHEN Purchase_Number = 1
                THEN Transaction_Date
            END
        ) AS First_Purchase,

        MAX(
            CASE
                WHEN Purchase_Number = 2
                THEN Transaction_Date
            END
        ) AS Second_Purchase

    FROM ranked_purchases

    GROUP BY CustomerID
)

SELECT
    COUNT(Second_Purchase) AS Repeat_Customers,

    ROUND(
        AVG(
            DATEDIFF(
                Second_Purchase,
                First_Purchase
            )
        ),
        1
    ) AS Avg_Days_To_Second_Purchase,

    MIN(
        DATEDIFF(
            Second_Purchase,
            First_Purchase
        )
    ) AS Min_Days,

    MAX(
        DATEDIFF(
            Second_Purchase,
            First_Purchase
        )
    ) AS Max_Days

FROM first_second_purchase

WHERE Second_Purchase IS NOT NULL;
