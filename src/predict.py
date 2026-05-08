import joblib
import pandas as pd

from src.realtime_features import extract_realtime_features
from src.utils.feature_extraction import extract_features


# ----------------------------
# LOAD MODELS + FEATURES
# ----------------------------
model_v2 = joblib.load("models/phish_model.pkl")
features_v2 = joblib.load("models/features.pkl")

model_v3 = joblib.load("models/phish_model_v3.pkl")
features_v3 = joblib.load("models/features_v3.pkl")


# ----------------------------
# INPUT
# ----------------------------
url = input("Enter URL: ").strip()

# ----------------------------
# INPUT VALIDATION
# ----------------------------
if not url:
    print("\n❌ Error: URL cannot be empty.")
    exit()

if "." not in url:
    print("\n❌ Error: Invalid URL format.")
    exit()

# ----------------------------
# V2 FEATURES (STATIC)
# ----------------------------
static_features = extract_features(url)
input_v2 = pd.DataFrame([static_features])[features_v2]

v2_prob = model_v2.predict_proba(input_v2)[0][1]


# ----------------------------
# V3 FEATURES (REAL-TIME)
# ----------------------------
realtime_features = extract_realtime_features(url)
input_v3 = pd.DataFrame([realtime_features])[features_v3]

v3_prob = model_v3.predict_proba(input_v3)[0][1]


# ----------------------------
# FINAL FUSION (CLEAN)
# ----------------------------
final_score = (0.7 * v2_prob) + (0.3 * v3_prob)


# ----------------------------
# FINAL DECISION
# ----------------------------
THRESHOLD = 0.5

if final_score > THRESHOLD:
    result = "⚠️ Phishing Website"
else:
    result = "✅ Safe Website"


# ----------------------------
# OUTPUT
# ----------------------------
print("\nRESULT:")
print(result)
print(f"Final Risk Score: {final_score:.2f}")

print("\n--- Debug Info ---")
print(f"V2 Probability: {v2_prob:.2f}")
print(f"V3 Probability: {v3_prob:.2f}")
print(f"Final Score: {final_score:.2f}")
print(f"Threshold: {THRESHOLD}")