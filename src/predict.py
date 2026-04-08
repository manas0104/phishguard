import joblib
import pandas as pd

from src.realtime_features import extract_realtime_features


# ----------------------------
# LOAD MODELS + FEATURES
# ----------------------------
model_v2 = joblib.load("models/phish_model.pkl")
features_v2 = joblib.load("models/features.pkl")

model_v3 = joblib.load("models/phish_model_v3.pkl")
features_v3 = joblib.load("models/features_v3.pkl")


# ----------------------------
# GET USER INPUT
# ----------------------------
url = input("Enter URL: ")


# ----------------------------
# EXTRACT REALTIME FEATURES (V3)
# ----------------------------
realtime_features = extract_realtime_features(url)

input_v3 = pd.DataFrame([realtime_features])
input_v3 = input_v3[features_v3]


# ----------------------------
# BUILD INPUT FOR V2 MODEL
# ----------------------------
input_data_v2 = {}

for feature in features_v2:

    if feature == "SSLfinal_State":
        input_data_v2[feature] = 1 if url.startswith("https") else 0

    elif feature == "URL_Length":
        input_data_v2[feature] = len(url)

    elif feature == "having_IP":
        input_data_v2[feature] = 1 if any(char.isdigit() for char in url) else 0

    elif feature == "having_Sub_Domain":
        input_data_v2[feature] = url.count('.') - 1

    elif feature == "Prefix_Suffix":
        input_data_v2[feature] = 1 if '-' in url else 0

    elif feature == "HTTPS_token":
        input_data_v2[feature] = 1 if "https" in url else 0

    else:
        input_data_v2[feature] = 0


input_v2 = pd.DataFrame([input_data_v2])
input_v2 = input_v2[features_v2]


# ----------------------------
# MODEL PREDICTIONS
# ----------------------------
pred_v2 = model_v2.predict(input_v2)[0]
prob_v2 = model_v2.predict_proba(input_v2)[0].max()

pred_v3 = model_v3.predict(input_v3)[0]
prob_v3 = model_v3.predict_proba(input_v3)[0].max()


# ----------------------------
# RULE-BASED SCORING
# ----------------------------
suspicion_score = 0

if "-" in url:
    suspicion_score += 1

if url.count('.') > 3:
    suspicion_score += 1

if not url.startswith("https"):
    suspicion_score += 1

if len(url) > 75:
    suspicion_score += 1


# ----------------------------
# HYBRID DECISION (IMPROVED)
# ----------------------------
score = 0

if pred_v2 == -1:
    score += prob_v2

if pred_v3 == -1:
    score += prob_v3

if suspicion_score >= 2:
    score += 0.5


# Final decision
if score > 0.8:
    final_pred = -1
else:
    final_pred = 1


# Confidence calculation
final_conf = max(prob_v2, prob_v3)


# ----------------------------
# OUTPUT
# ----------------------------
print("\nRESULT:")

if final_pred == 1:
    print("Safe Website")
else:
    print("Phishing Website")

print(f"Confidence: {final_conf * 100:.2f}%")


# ----------------------------
# DEBUG INFO
# ----------------------------
print("\n--- Debug Info ---")
print(f"V2 Prediction: {pred_v2} (Confidence: {prob_v2:.2f})")
print(f"V3 Prediction: {pred_v3} (Confidence: {prob_v3:.2f})")
print(f"Suspicion Score: {suspicion_score}")
print(f"Final Score: {score:.2f}")