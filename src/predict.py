import joblib
import pandas as pd
from feature_extraction import extract_features

# Load model
model = joblib.load("models/phish_model.pkl")

print("🔐 PhishGuard is ready!")

try:
    # Take URL input
    url = input("Enter URL: ").strip()

    if not url:
        raise ValueError("URL cannot be empty")

    # Extract features
    features = extract_features(url)

    # Get feature names
    feature_names = model.feature_names_in_

    # Convert to DataFrame
    input_df = pd.DataFrame([features], columns=feature_names)

    # Predict
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)

    # Confidence
    confidence = max(probability[0]) * 100

    # Output
    print("\n🔍 RESULT:")
    if prediction[0] == 1:
        print("⚠️ Phishing Website Detected!")
    else:
        print("✅ Safe Website")

    print(f"📊 Confidence: {confidence:.2f}%")

except Exception as e:
    print("❌ Error:", str(e))