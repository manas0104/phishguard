import joblib
import pandas as pd
from feature_extraction import extract_features

# Load model + selected features
model = joblib.load("models/phish_model.pkl")
selected_features = joblib.load("models/features.pkl")

print("🔐 PhishGuard V2 is ready!")

try:
    url = input("Enter URL: ").strip()

    if not url:
        raise ValueError("URL cannot be empty")

    # Extract features
    feature_dict = extract_features(url)

    # Convert to DataFrame
    features_df = pd.DataFrame([feature_dict])

    # Ensure correct order
    features_df = features_df[selected_features]

    # Predict
    prediction = model.predict(features_df)
    confidence = model.predict_proba(features_df)[0].max() * 100

    print("\n🔍 RESULT:")

    if prediction[0] == 1:
        print("⚠️ Phishing Website Detected!")
    else:
        print("✅ Safe Website")

    print(f"📊 Confidence: {confidence:.2f}%")

except Exception as e:
    print("❌ Error:", str(e))