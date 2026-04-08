import pandas as pd
import joblib
import time

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from src.realtime_features import extract_realtime_features


print("Loading dataset...")
df = pd.read_csv("data/url_dataset.csv")


# ----------------------------
# FEATURE EXTRACTION (OPTIMIZED)
# ----------------------------
print("Extracting features...")

feature_cache = {}   # 🔥 cache to avoid repeated calls
features = []

for i, url in enumerate(df['url']):

    if url in feature_cache:
        f = feature_cache[url]
    else:
        try:
            f = extract_realtime_features(url)
        except:
            f = {
                "domain_age": -1,
                "has_mx": 0,
                "has_ip": 0
            }

        feature_cache[url] = f
        time.sleep(0.1)  # avoid blocking

    features.append(f)

    if i % 25 == 0:
        print(f"Processed {i}/{len(df)}")


X = pd.DataFrame(features)
y = df['label']


# ----------------------------
# TRAIN
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training model...")

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))


# ----------------------------
# SAVE
# ----------------------------
joblib.dump(model, "models/phish_model_v3.pkl")
joblib.dump(list(X.columns), "models/features_v3.pkl")

print("V3 model saved!")