# ============================================
# 02. STATISTICAL ANALYSIS
# Retail Demand Intelligence
# ============================================

import pandas as pd
import numpy as np

from scipy import stats
import statsmodels.api as sm


# --------------------------------------------
# Load transaction data
# --------------------------------------------

df = pd.read_csv("data/Retail_Transaction_Dataset.csv")


df["TransactionDate"] = pd.to_datetime(
    df["TransactionDate"],
    format="mixed"
)


# ============================================
# 1. Descriptive Statistics
# ============================================

print("Descriptive Statistics")
print("----------------------")

print(
    df[
        [
            "Quantity",
            "Price",
            "DiscountApplied(%)",
            "TotalAmount"
        ]
    ].describe().round(2)
)


# ============================================
# 2. ANOVA
# Does discount level affect quantity?
# ============================================

df["Discount_Group"] = pd.cut(
    df["DiscountApplied(%)"],
    bins=[-0.01, 5, 10, 15, 20],
    labels=[
        "0-5%",
        "5-10%",
        "10-15%",
        "15-20%"
    ]
)

groups = [
    group["Quantity"].values
    for _, group in df.groupby(
        "Discount_Group",
        observed=True
    )
]

f_stat, p_value = stats.f_oneway(*groups)

print("\nANOVA: Discount vs Quantity")
print("----------------------------")
print("F-statistic:", round(f_stat, 3))
print("p-value:", round(p_value, 3))


# ============================================
# 3. Welch's t-test
# New vs Returning Customer AOV
# ============================================

df = df.sort_values(
    ["CustomerID", "TransactionDate"]
)

df["Purchase_Number"] = (
    df.groupby("CustomerID")
      .cumcount() + 1
)

new_customer_aov = df.loc[
    df["Purchase_Number"] == 1,
    "TotalAmount"
]

returning_customer_aov = df.loc[
    df["Purchase_Number"] > 1,
    "TotalAmount"
]

t_stat, t_p_value = stats.ttest_ind(
    new_customer_aov,
    returning_customer_aov,
    equal_var=False
)

print("\nWelch's t-test: New vs Returning AOV")
print("-------------------------------------")
print("t-statistic:", round(t_stat, 3))
print("p-value:", round(t_p_value, 3))


# ============================================
# 4. Chi-Square Test
# Customer Type vs Category
# ============================================

df["Customer_Type"] = np.where(
    df["Purchase_Number"] == 1,
    "New",
    "Returning"
)

contingency_table = pd.crosstab(
    df["Customer_Type"],
    df["ProductCategory"]
)

chi2, chi_p_value, dof, expected = (
    stats.chi2_contingency(contingency_table)
)

print("\nChi-Square: Customer Type vs Category")
print("--------------------------------------")
print("Chi-square:", round(chi2, 3))
print("Degrees of freedom:", dof)
print("p-value:", round(chi_p_value, 3))


# ============================================
# 5. Regression
# Quantity ~ Discount + Price
# ============================================

X = df[
    [
        "DiscountApplied(%)",
        "Price"
    ]
]

X = sm.add_constant(X)

y = df["Quantity"]

regression_model = sm.OLS(
    y,
    X
).fit()

print("\nRegression: Quantity vs Discount & Price")
print("-----------------------------------------")

print(
    regression_model.summary()
)
