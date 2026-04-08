from src.realtime_features import extract_realtime_features
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from src.preprocess import preprocess_data


print("Loading dataset...")
df = pd.read_csv("data/phishing.csv")

# ----------------------------
# CHECK URL COLUMN
# ----------------------------
if 'url' not in df.columns:
    print("⚠️ WARNING: 'url' column not found. Skipping realtime features.")
else:
    print("Adding realtime features...")

    realtime_data = df['url'].apply(extract_realtime_features)
    realtime_df = pd.DataFrame(realtime_data.tolist())

    df = pd.concat([df, realtime_df], axis=1)


# ----------------------------
# PREPROCESS
# ----------------------------
df = preprocess_data(df)


# ----------------------------
# FEATURES & TARGET
# ----------------------------
X = df.drop(['Result'], axis=1)
y = df['Result']


# ----------------------------
# TRAIN TEST SPLIT
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# ----------------------------
# TRAIN MODEL (ALL FEATURES)
# ----------------------------
print("\nTraining model (all features)...")

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nInitial Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# ----------------------------
# FEATURE IMPORTANCE
# ----------------------------
print("\nCalculating feature importance...")

importance = model.feature_importances_
feature_names = X.columns

feat_imp = pd.Series(importance, index=feature_names)
feat_imp = feat_imp.sort_values(ascending=False)

print("\nTop Features:\n", feat_imp.head(20))


# ----------------------------
# SELECT BEST FEATURES
# ----------------------------
TOP_N = 15
selected_features = feat_imp.head(TOP_N).index.tolist()

print("\nSelected Features:\n", selected_features)


# ----------------------------
# RETRAIN MODEL
# ----------------------------
print("\nRetraining with selected features...")

X_selected = X[selected_features]

X_train, X_test, y_train, y_test = train_test_split(
    X_selected, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nFinal Accuracy:", accuracy_score(y_test, y_pred))
print("\nFinal Classification Report:\n", classification_report(y_test, y_pred))


# ----------------------------
# SAVE MODEL + FEATURES
# ----------------------------
joblib.dump(model, "models/phish_model.pkl")
joblib.dump(selected_features, "models/features.pkl")

print("\nModel + features saved successfully!")