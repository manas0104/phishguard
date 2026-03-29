import pandas as pd
import numpy as np


def preprocess_data(df):
    print("\n Starting preprocessing...")

    # ----------------------------
    # 1. DROP USELESS COLUMNS
    # ----------------------------
    if 'index' in df.columns:
        df = df.drop(['index'], axis=1)
        print("✔ Dropped 'index' column")

    # ----------------------------
    # 2. HANDLE MISSING VALUES
    # ----------------------------
    missing = df.isnull().sum().sum()

    if missing > 0:
        print(f"⚠ Found {missing} missing values")

        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype == 'object':
                    df[col].fillna(df[col].mode()[0], inplace=True)
                else:
                    df[col].fillna(df[col].median(), inplace=True)

        print("✔ Missing values handled...")
    else:
        print("✔ No missing values.")

    # ----------------------------
    # 3. REMOVE DUPLICATES
    # ----------------------------
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]

    if before != after:
        print(f"✔ Removed {before - after} duplicate rows")
    else:
        print("✔ No duplicates found")

    # ----------------------------
    # 4. ENCODE CATEGORICAL DATA
    # ----------------------------
    categorical_cols = df.select_dtypes(include=['object']).columns

    if len(categorical_cols) > 0:
        print(f"Encoding categorical columns: {list(categorical_cols)}")

        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

        print("✔ Encoding complete")
    else:
        print("✔ No categorical columns")

    # ----------------------------
    # 5. CHECK DATA TYPES
    # ----------------------------
    print("\n Data types:\n", df.dtypes)

    # ----------------------------
    # 6. OUTLIER HANDLING (OPTIONAL)
    # ----------------------------
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df[col] = np.where(df[col] < lower, lower, df[col])
        df[col] = np.where(df[col] > upper, upper, df[col])

    print("✔ Outlier handling applied (if needed)")

    print("\n Preprocessing completed...\n")

    return df