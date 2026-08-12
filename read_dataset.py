import pandas as pd

# Read the dataset
df = pd.read_csv("dataset/flowers_dataset.csv")

# Display first 5 rows
print("First 5 Records")
print(df.head())

# Dataset shape
print("\nDataset Shape:")
print(df.shape)

# Column names
print("\nColumns:")
print(df.columns)

# Data types
print("\nData Types:")
print(df.dtypes)

# Missing Values check
print("\nMissing Values:")
print(df.isnull().sum())
print(df.isnull().sum().sum())

