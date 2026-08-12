import pandas as pd
import numpy as np

# ============================================================
# LOAD DATASETS
# ============================================================

MAIN_FILE = "dataset/flowers_dataset.csv"
FLOWERS_FILE = "dataset/design_flowers.csv"
PRICES_FILE = "dataset/flower_prices.csv"

OUTPUT_FILE = "dataset/pookalam_processed.csv"

df = pd.read_csv(MAIN_FILE)
design_flowers = pd.read_csv(FLOWERS_FILE)
flower_prices = pd.read_csv(PRICES_FILE)

print("=" * 70)
print("POOKALAM DATA PREPROCESSING")
print("=" * 70)

print("\nMain dataset loaded successfully.")
print("Original shape:", df.shape)


# ============================================================
# BASIC VALIDATION
# ============================================================

if df["design_id"].duplicated().any():
    raise ValueError("Duplicate design IDs found.")

if df.isna().sum().sum() > 0:
    raise ValueError("Missing values found in main dataset.")

print("✓ No missing values")
print("✓ No duplicate design IDs")


# ============================================================
# FEATURE 1: FLOWER DIVERSITY
# ============================================================

df["flower_diversity"] = df[
    [
        "primary_flower",
        "secondary_flower",
        "accent_flower"
    ]
].nunique(axis=1)


# ============================================================
# FEATURE 2: COLOR DIVERSITY
# ============================================================

df["color_diversity"] = df[
    [
        "primary_color",
        "secondary_color",
        "accent_color"
    ]
].nunique(axis=1)


# ============================================================
# FEATURE 3: ESTIMATED FLOWER COST
# ============================================================

print("\nCalculating estimated flower cost...")


# Create flower → price dictionary

price_lookup = dict(
    zip(
        flower_prices["flower"],
        flower_prices["price_per_kg"]
    )
)


# Check every flower has a price

flowers_used = set(
    design_flowers["flower"].dropna()
)

missing_prices = sorted(
    flowers_used - set(price_lookup.keys())
)

if missing_prices:

    raise ValueError(
        f"Missing prices for flowers: {missing_prices}"
    )

print("✓ All flowers have valid prices")


# Map price to flower composition

design_flowers["price_per_kg"] = (
    design_flowers["flower"]
    .map(price_lookup)
)


# Calculate cost for each flower

design_flowers["flower_cost"] = (
    design_flowers["quantity_kg"]
    * design_flowers["price_per_kg"]
)


# Calculate total flower cost for each design

flower_cost = (
    design_flowers
    .groupby("design_id")["flower_cost"]
    .sum()
    .reset_index()
)


flower_cost.rename(
    columns={
        "flower_cost": "estimated_flower_cost"
    },
    inplace=True
)


# Merge with main dataset

df = df.merge(
    flower_cost,
    on="design_id",
    how="left"
)


df["estimated_flower_cost"] = (
    df["estimated_flower_cost"]
    .round(2)
)


# Validate flower cost

if df["estimated_flower_cost"].isna().any():

    missing_ids = df.loc[
        df["estimated_flower_cost"].isna(),
        "design_id"
    ].tolist()

    raise ValueError(
        f"Flower cost missing for design IDs: {missing_ids}"
    )

print("✓ Estimated flower cost calculated")


# ============================================================
# DISPLAY ENGINEERED FEATURES
# ============================================================

new_features = [
    "flower_diversity",
    "color_diversity",
    "estimated_flower_cost"
]

print("\n" + "=" * 70)
print("ENGINEERED FEATURES")
print("=" * 70)

print(
    df[
        [
            "design_id",
            "theme",
            "style",
            "budget"
        ] + new_features
    ].head(10)
)


# ============================================================
# DATASET SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATASET SUMMARY")
print("=" * 70)

print("\nFinal shape:", df.shape)

print("\nThemes:")
print(df["theme"].value_counts())


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL VALIDATION")
print("=" * 70)

missing_values = df.isna().sum().sum()
duplicate_rows = df.duplicated().sum()
duplicate_ids = df["design_id"].duplicated().sum()
design_count = df["design_id"].nunique()

print("Missing values:", missing_values)
print("Duplicate rows:", duplicate_rows)
print("Duplicate design IDs:", duplicate_ids)
print("Design count:", design_count)

if (
    missing_values == 0
    and duplicate_rows == 0
    and duplicate_ids == 0
    and len(df) == design_count
):
    print("\n✓ DATA VALIDATION PASSED")
else:
    raise ValueError("Dataset validation failed.")


# ============================================================
# SAVE PROCESSED DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nProcessed dataset saved successfully.")

print(
    "Output:",
    OUTPUT_FILE
)

print(
    "Final shape:",
    df.shape
)

print("\nColumns:")

for i, column in enumerate(
    df.columns,
    1
):

    print(
        i,
        column
    )

print("\n✓ PREPROCESSING COMPLETED")