import pandas as pd

# Load dataset
df = pd.read_csv("data/phishing.csv")

# Show first 5 rows
print(df.head())

# Show shape
print("\nShape:", df.shape)

# Show column names
print("\nColumns:", df.columns)