# ============================================================
# AI POOKALAM DESIGNER
# Exploratory Data Analysis (EDA)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------

DATA_PATH = Path("dataset/flowers_dataset.csv")

df = pd.read_csv(DATA_PATH)

print("\n" + "=" * 70)
print("AI POOKALAM DESIGNER - EXPLORATORY DATA ANALYSIS")
print("=" * 70)

print("\nDataset loaded successfully.")
print("Shape:", df.shape)


# ------------------------------------------------------------
# 2. BASIC INFORMATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("1. BASIC INFORMATION")
print("=" * 70)

print("\nNumber of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nColumns:")
for col in df.columns:
    print("-", col)

print("\nData types:")
print(df.dtypes)


# ------------------------------------------------------------
# 3. FIRST FEW RECORDS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("2. FIRST 5 RECORDS")
print("=" * 70)

print(df.head())


# ------------------------------------------------------------
# 4. LAST FEW RECORDS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("3. LAST 5 RECORDS")
print("=" * 70)

print(df.tail())


# ------------------------------------------------------------
# 5. MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("4. MISSING VALUES")
print("=" * 70)

missing_values = df.isnull().sum()

print(missing_values)

total_missing = missing_values.sum()

print("\nTotal missing values:", total_missing)

if total_missing == 0:
    print("✓ No missing values found.")
else:
    print("⚠ Missing values found. Review before preprocessing.")


# ------------------------------------------------------------
# 6. DUPLICATE RECORDS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("5. DUPLICATE RECORDS")
print("=" * 70)

duplicate_rows = df.duplicated().sum()

print("Duplicate rows:", duplicate_rows)

if duplicate_rows == 0:
    print("✓ No duplicate rows found.")
else:
    print("⚠ Duplicate rows found.")


# ------------------------------------------------------------
# 7. DUPLICATE DESIGN IDs
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("6. DUPLICATE DESIGN IDs")
print("=" * 70)

duplicate_ids = df["design_id"].duplicated().sum()

print("Duplicate design IDs:", duplicate_ids)

if duplicate_ids == 0:
    print("✓ All design IDs are unique.")
else:
    print("⚠ Duplicate design IDs found.")

    print(
        df[df["design_id"].duplicated(keep=False)]
        [["design_id", "design_name"]]
        .sort_values("design_id")
    )


# ------------------------------------------------------------
# 8. UNIQUE VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("7. UNIQUE VALUES")
print("=" * 70)

categorical_columns = [
    "theme",
    "style",
    "difficulty",
    "primary_flower",
    "secondary_flower",
    "accent_flower",
    "primary_color",
    "secondary_color",
    "accent_color",
    "occasion"
]

for column in categorical_columns:

    if column in df.columns:

        print(f"\n{column.upper()}")

        print(df[column].unique())

        print("Number of unique values:",
              df[column].nunique())


# ------------------------------------------------------------
# 9. THEME DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("8. THEME DISTRIBUTION")
print("=" * 70)

theme_counts = df["theme"].value_counts()

print(theme_counts)

print("\nPercentage distribution:")

theme_percentage = (
    df["theme"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(theme_percentage)


# ------------------------------------------------------------
# 10. NEW THEME CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("9. NEW THEME CHECK")
print("=" * 70)

new_themes = [
    "Kathakali",
    "Vallamkali",
    "Nilavilakku",
    "Nature",
    "Wild"
]

for theme in new_themes:

    count = (df["theme"] == theme).sum()

    print(f"{theme:<15} : {count}")

    if count > 0:
        print("  ✓ Theme present")
    else:
        print("  ⚠ Theme missing")


# ------------------------------------------------------------
# 11. STYLE / PATTERN DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("10. STYLE / PATTERN DISTRIBUTION")
print("=" * 70)

print(df["style"].value_counts())


# ------------------------------------------------------------
# 12. CHECK THEME/STYLE SEPARATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("11. THEME / STYLE CONSISTENCY CHECK")
print("=" * 70)

# These values should ideally belong to Theme,
# not Style/Pattern.
new_theme_values = set(new_themes)

wrong_style_records = df[
    df["style"].isin(new_theme_values)
]

if len(wrong_style_records) == 0:

    print("✓ No new-theme values found in the Style column.")

else:

    print(
        "⚠ The following records have Theme values "
        "stored in the Style column:"
    )

    print(
        wrong_style_records[
            [
                "design_id",
                "design_name",
                "theme",
                "style"
            ]
        ].to_string(index=False)
    )


# ------------------------------------------------------------
# 13. DIFFICULTY DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("12. DIFFICULTY DISTRIBUTION")
print("=" * 70)

print(df["difficulty"].value_counts())


# ------------------------------------------------------------
# 14. OCCASION DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("13. OCCASION DISTRIBUTION")
print("=" * 70)

print(df["occasion"].value_counts())


# ------------------------------------------------------------
# 15. NUMERICAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("14. NUMERICAL SUMMARY")
print("=" * 70)

numeric_columns = [
    "budget",
    "layers",
    "diameter_ft",
    "estimated_time_hr",
    "people_required"
]

print(
    df[numeric_columns]
    .describe()
    .round(2)
)


# ------------------------------------------------------------
# 16. NEGATIVE / ZERO VALUE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("15. INVALID NUMERICAL VALUES")
print("=" * 70)

for column in numeric_columns:

    invalid = (df[column] <= 0).sum()

    print(f"{column:<20} : {invalid} invalid values")

    if invalid == 0:
        print("  ✓ Valid")
    else:
        print("  ⚠ Check these records")


# ------------------------------------------------------------
# 17. FLOWER DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("16. FLOWER USAGE")
print("=" * 70)

flower_columns = [
    "primary_flower",
    "secondary_flower",
    "accent_flower"
]

all_flowers = pd.concat(
    [
        df[column]
        for column in flower_columns
    ]
)

print(
    all_flowers
    .value_counts()
)


# ------------------------------------------------------------
# 18. COLOR DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("17. COLOR USAGE")
print("=" * 70)

color_columns = [
    "primary_color",
    "secondary_color",
    "accent_color"
]

all_colors = pd.concat(
    [
        df[column]
        for column in color_columns
    ]
)

print(
    all_colors
    .value_counts()
)


# ------------------------------------------------------------
# 19. NEW THEME NUMERICAL ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("18. NEW THEMES - NUMERICAL ANALYSIS")
print("=" * 70)

new_theme_df = df[
    df["theme"].isin(new_themes)
]

print(
    new_theme_df[
        [
            "theme",
            "budget",
            "layers",
            "diameter_ft",
            "estimated_time_hr",
            "people_required"
        ]
    ]
    .groupby("theme")
    .mean()
    .round(2)
)


# ------------------------------------------------------------
# 20. NEW THEME × STYLE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("19. NEW THEME × STYLE")
print("=" * 70)

theme_style_table = pd.crosstab(
    new_theme_df["theme"],
    new_theme_df["style"]
)

print(theme_style_table)


# ------------------------------------------------------------
# 21. THEME × DIFFICULTY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("20. THEME × DIFFICULTY")
print("=" * 70)

theme_difficulty = pd.crosstab(
    df["theme"],
    df["difficulty"]
)

print(theme_difficulty)


# ------------------------------------------------------------
# 22. THEME × OCCASION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("21. THEME × OCCASION")
print("=" * 70)

theme_occasion = pd.crosstab(
    df["theme"],
    df["occasion"]
)

print(theme_occasion)


# ------------------------------------------------------------
# 23. BUDGET BY THEME
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("22. AVERAGE BUDGET BY THEME")
print("=" * 70)

budget_by_theme = (
    df.groupby("theme")["budget"]
    .agg(["count", "mean", "min", "max"])
    .round(2)
)

print(budget_by_theme)


# ------------------------------------------------------------
# 24. CORRELATION MATRIX
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("23. NUMERICAL CORRELATION")
print("=" * 70)

correlation = (
    df[numeric_columns]
    .corr()
    .round(2)
)

print(correlation)


# ------------------------------------------------------------
# 25. OUTLIER CHECK USING IQR
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("24. OUTLIER CHECK")
print("=" * 70)

for column in numeric_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower) |
        (df[column] > upper)
    ]

    print(
        f"{column:<20} : {len(outliers)} outliers"
    )


# ============================================================
# VISUALIZATIONS
# ============================================================

# ------------------------------------------------------------
# 26. THEME DISTRIBUTION
# ------------------------------------------------------------

plt.figure(figsize=(11, 6))

df["theme"].value_counts().plot(
    kind="bar"
)

plt.title("Pookalam Theme Distribution")
plt.xlabel("Theme")
plt.ylabel("Number of Designs")
plt.xticks(rotation=35)

plt.tight_layout()

plt.savefig(
    "theme_distribution.png",
    dpi=150
)

plt.show()


# ------------------------------------------------------------
# 27. DIFFICULTY DISTRIBUTION
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

df["difficulty"].value_counts().plot(
    kind="bar"
)

plt.title("Difficulty Distribution")
plt.xlabel("Difficulty")
plt.ylabel("Number of Designs")

plt.tight_layout()

plt.savefig(
    "difficulty_distribution.png",
    dpi=150
)

plt.show()


# ------------------------------------------------------------
# 28. BUDGET DISTRIBUTION
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

df["budget"].plot(
    kind="hist",
    bins=20
)

plt.title("Budget Distribution")
plt.xlabel("Budget")
plt.ylabel("Number of Designs")

plt.tight_layout()

plt.savefig(
    "budget_distribution.png",
    dpi=150
)

plt.show()


# ------------------------------------------------------------
# 29. THEME VS BUDGET
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

df.boxplot(
    column="budget",
    by="theme",
    rot=35
)

plt.title("Budget Distribution by Theme")
plt.suptitle("")

plt.xlabel("Theme")
plt.ylabel("Budget")

plt.tight_layout()

plt.savefig(
    "budget_by_theme.png",
    dpi=150
)

plt.show()


# ------------------------------------------------------------
# 30. THEME × DIFFICULTY HEATMAP
# ------------------------------------------------------------

plt.figure(figsize=(12, 7))

plt.imshow(
    theme_difficulty.values,
    aspect="auto"
)

plt.colorbar(
    label="Number of Designs"
)

plt.xticks(
    range(len(theme_difficulty.columns)),
    theme_difficulty.columns,
    rotation=30
)

plt.yticks(
    range(len(theme_difficulty.index)),
    theme_difficulty.index
)

plt.title("Theme vs Difficulty")

plt.tight_layout()

plt.savefig(
    "theme_difficulty_heatmap.png",
    dpi=150
)

plt.show()


# ------------------------------------------------------------
# 31. FINAL EDA SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EDA COMPLETED")
print("=" * 70)

print(
    f"""
Dataset:
    Rows              : {df.shape[0]}
    Columns           : {df.shape[1]}

Data Quality:
    Missing values    : {total_missing}
    Duplicate rows    : {duplicate_rows}
    Duplicate IDs     : {duplicate_ids}

New Themes:
    Kathakali
    Vallamkali
    Nilavilakku
    Nature
    Wild

Next step:
    1. Fix any theme/style inconsistencies
    2. Validate design_flowers.csv IDs
    3. Feature engineering
    4. Preprocessing
    5. Train ML models
"""
)

print("=" * 70)