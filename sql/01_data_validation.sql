USE retail_demand_intelligence;

-- ============================================
-- 01. DATA VALIDATION
-- ============================================

-- Total number of transactions
SELECT
    COUNT(*) AS Total_Transactions
FROM retail_transactions;


-- Date range
SELECT
    MIN(Transaction_Date) AS Start_Date,
    MAX(Transaction_Date) AS End_Date
FROM retail_transactions;


-- Unique customers
SELECT
    COUNT(DISTINCT CustomerID) AS Unique_Customers
FROM retail_transactions;


-- Unique products
SELECT
    COUNT(DISTINCT ProductID) AS Unique_Products
FROM retail_transactions;


-- Unique categories
SELECT
    COUNT(DISTINCT ProductCategory) AS Unique_Categories
FROM retail_transactions;


-- Unique payment methods
SELECT
    COUNT(DISTINCT PaymentMethod) AS Unique_Payment_Methods
FROM retail_transactions;


-- Check for missing values
SELECT
    SUM(CustomerID IS NULL) AS Missing_CustomerID,
    SUM(ProductID IS NULL) AS Missing_ProductID,
    SUM(Quantity IS NULL) AS Missing_Quantity,
    SUM(Price IS NULL) AS Missing_Price,
    SUM(Transaction_Date IS NULL) AS Missing_Transaction_Date,
    SUM(PaymentMethod IS NULL) AS Missing_PaymentMethod,
    SUM(ProductCategory IS NULL) AS Missing_Category,
    SUM(DiscountApplied IS NULL) AS Missing_Discount,
    SUM(TotalAmount IS NULL) AS Missing_TotalAmount
FROM retail_transactions;


-- Check for duplicate transaction rows
SELECT
    COUNT(*) - COUNT(
        DISTINCT CONCAT(
            CustomerID,
            ProductID,
            Transaction_Date,
            Quantity,
            Price,
            TotalAmount
        )
    ) AS Duplicate_Rows
FROM retail_transactions;
