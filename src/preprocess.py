import pandas as pd
import numpy as np


def preprocess_data(df):
    print("\n Starting preprocessing...")

    # ----------------------------
    # 0. FIX COLUMN NAMES (CRITICAL)
    # ----------------------------
    df = df.rename(columns={
        'having_IPhaving_IP_Address': 'having_IP'
    })

    # ----------------------------
    # 1. DROP USELESS COLUMNS
    # ----------------------------
    if 'index' in df.columns:
        df = df.drop(columns=['index'])
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
                    df[col] = df[col].fillna(df[col].mode()[0])
                else:
                    df[col] = df[col].fillna(df[col].median())

        print("✔ Missing values handled")
    else:
        print("✔ No missing values")

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
    # 5. ENSURE NUMERIC TYPES
    # ----------------------------
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    print("\n Data types:\n", df.dtypes)

    # ----------------------------
    # 6. OUTLIER HANDLING (SAFE)
    # ----------------------------
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if col == 'Result':  # ❗ Do not modify target
            continue

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue  # skip constant columns

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df[col] = np.clip(df[col], lower, upper)

    print("✔ Outlier handling applied (safe)")

    print("\n Preprocessing completed...\n")

    return df