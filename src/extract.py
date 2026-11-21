
# ============================================================
# RETAIL DATA ETL PIPELINE - EXTRACT & VALIDATE
#
# Purpose:
# 1. Read raw order data from CSV
# 2. Identify invalid records
# 3. Assign error reasons to rejected records
# 4. Separate valid and rejected records
# 5. Save cleaned datasets as CSV files
# 6. Perform final data quality checks
# ============================================================


# STEP 1: Import required libraries
# pandas is used to read, validate and transform CSV data.

import pandas as pd


# STEP 2: Read raw order data
# order.csv contains the original retail transactions.
# The DataFrame stores all rows and columns from the CSV.

order_df = pd.read_csv("data/order.csv")

print("Total source records:", len(order_df))


# STEP 3: Define data validation conditions
# Each condition returns True for records that fail a rule.

# Rule 1: Quantity must not be missing.
condition1 = order_df["quantity"].isna()

# Rule 2: Unit price must not be negative.
condition2 = order_df["unit_price"] < 0

# Rule 3: Customer ID must not be missing.
condition3 = order_df["customer_id"].isna()

# Rule 4: Order ID must not be duplicated.
# The first occurrence is retained.
# Later occurrences of the same order ID are rejected.
condition4 = order_df.duplicated(
    subset=["order_id"]
)


# STEP 4: Identify invalid and valid records
# | (OR) combines all validation conditions.
# A record is invalid if any condition is True.
# ~ (NOT) reverses the Boolean result.

invalid_rows = (
    condition1 |
    condition2 |
    condition3 |
    condition4
)

valid_rows = ~invalid_rows


# STEP 5: Generate data quality summary
# Count how many records failed each validation rule.

report = {
    "Total source records": len(order_df),
    "Missing quantity": condition1.sum(),
    "Negative unit prices": condition2.sum(),
    "Missing customer IDs": condition3.sum(),
    "Duplicate order IDs": condition4.sum(),
    "Total rejected records": invalid_rows.sum(),
    "Total valid records": valid_rows.sum()
}

print("\nDATA QUALITY REPORT")

for key, value in report.items():
    print(f"{key}: {value}")


# STEP 6: Create error_reason column
# Every rejected record should explain why it failed.
# A record can contain multiple error reasons.

order_df["error_reason"] = ""

order_df.loc[
    condition1, "error_reason"
] += "Missing quantity; "

order_df.loc[
    condition2, "error_reason"
] += "Negative unit price; "

order_df.loc[
    condition3, "error_reason"
] += "Missing customer ID; "

order_df.loc[
    condition4, "error_reason"
] += "Duplicate order ID; "


# STEP 7: Calculate validation failure count
# Convert True/False into 1/0 using astype(int).
# Sum the conditions to count failures per record.

order_df["failure_count"] = (
    condition1.astype(int)
    + condition2.astype(int)
    + condition3.astype(int)
    + condition4.astype(int)
)


# STEP 8: Separate valid and rejected records
# Valid records pass all validation conditions.
# Rejected records fail at least one condition.
# copy() creates independent DataFrames.

valid_df = order_df.loc[valid_rows].copy()

rejected_df = order_df.loc[invalid_rows].copy()


# STEP 9: Verify data quality before exporting
# Raise an exception if any quality check fails.
# This prevents the pipeline from continuing
# with inconsistent or incomplete data.

# Check 1: No records were lost during separation.
if len(order_df) != len(valid_df) + len(rejected_df):
    raise ValueError("FAIL: Record count mismatch")

print("PASS: Record count matched")


# Check 2: Every rejected record has an error reason.
if not rejected_df["error_reason"].fillna(
    ""
).str.strip().ne("").all():
    raise ValueError(
        "FAIL: Rejected records missing error reasons"
    )

print("PASS: All rejected records have error reasons")


# Check 3: Valid order IDs must be unique.
if not valid_df["order_id"].is_unique:
    raise ValueError("FAIL: Duplicate valid order IDs")

print("PASS: All valid order IDs are unique")


# STEP 10: Export validated datasets
# index=False prevents Pandas row indexes
# from being written as an additional CSV column.
#
# Export happens only after quality checks pass.

valid_df.to_csv(
    "data/valid_df.csv",
    index=False
)

rejected_df.to_csv(
    "data/rejected_df.csv",
    index=False
)


# STEP 11: Display final execution summary

print("\nEXTRACTION COMPLETED SUCCESSFULLY")
print("Valid records exported:", len(valid_df))
print("Rejected records exported:", len(rejected_df))
print("All data quality checks passed!")
