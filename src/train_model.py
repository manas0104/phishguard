import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from preprocess import preprocess_data

# ----------------------------
# LOAD DATA
# ----------------------------
print(" Loading dataset...")
df = pd.read_csv("data/phishing.csv")

# ----------------------------
# PREPROCESSING
# ----------------------------
df = preprocess_data(df)

# ----------------------------
# FEATURES & TARGET
# ----------------------------
print(" Splitting features and target...")

X = df.drop(['Result'], axis=1)
y = df['Result']

# ----------------------------
# TRAIN-TEST SPLIT
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(" Training samples:", X_train.shape[0])
print(" Testing samples:", X_test.shape[0])

# ----------------------------
# MODEL TRAINING
# ----------------------------
print("\n Training Random Forest model...")

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ----------------------------
# PREDICTION
# ----------------------------
print(" Making predictions...")
y_pred = model.predict(X_test)

# ----------------------------
# EVALUATION
# ----------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\n Model Accuracy:", accuracy)

print("\n Classification Report:")
print(classification_report(y_test, y_pred))

joblib.dump(model, "models/phish_model.pkl")
print("\n Model saved successfully!")