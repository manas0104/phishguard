
# PhishGuard – Hybrid Phishing Detection System

PhishGuard is a hybrid machine learning-based phishing detection system that combines:
	•	Static feature-based ML (V2)
	•	Real-time domain intelligence (V3)
	•	Rule-based heuristics

to detect phishing URLs with improved robustness and real-world applicability.

---

## Features
	•	Detect phishing URLs in real-time
	•	Dual-model architecture (V2 + V3)
	•	WHOIS, DNS, IP-based feature extraction
	•	Hybrid decision logic (ML + rules)
	•	Confidence scoring
	•	Debug insights for explainability
---

## System Architecture

```txt
                ┌──────────────┐
URL ───────────▶│ V2 Features  │──▶ Model V2
                │ (Static ML)  │
                └──────────────┘

                ┌──────────────┐
URL ───────────▶│ V3 Features  │──▶ Model V3
                │ (Realtime)   │
                └──────────────┘

                        ↓
                Hybrid Decision Logic
                        ↓
                Rule-based Override
                        ↓
                  Final Prediction
```
---

## Project Structure
```txt
PhishGuard/
│
├── data/
│   ├── url_dataset.csv          # Final dataset (used for V3 training)
│   ├── phishing_cleaned.csv     # Cleaned phishing data (reference)
│   └── phishing.csv             # Raw dataset (V2)
│
├── models/
│   ├── phish_model.pkl          # V2 model
│   ├── features.pkl             # V2 features
│   ├── phish_model_v3.pkl       # V3 model (real-time)
│   └── features_v3.pkl          # V3 features
│
├── src/
│   ├── __init__.py              # Makes src a package
│   ├── predict.py               # Main prediction system (HYBRID)
│   ├── train_model.py           # V2 model training
│   ├── train_url_model.py       # V3 model training
│   ├── realtime_features.py     # Real-time feature extraction
│   ├── preprocess.py            # Data preprocessing
│   │
│   └── utils/                   # Helper modules
│       ├── feature_extraction.py
│       └── load_data.py
│
├── Requirements.txt             # Dependencies
├── README.md                    # Project documentation
└── .gitignore                   # Ignore unnecessary files
```
---

## Installation
```txt
git clone https://github.com/manas0104/phishguard.git
cd phishguard

pip install -r requirements.txt
```
   
---

## Usage

Predict URL: 
python3 -m src.predict

---

## Example
```txt
Enter URL: http://google.com

RESULT:
Phishing Website
Confidence: 79.21%

--- Debug Info ---
V2 Prediction: -1
V3 Prediction: 1
Suspicion Score: 1
Final Score: 1.36
```
---

## Models

V2 Model
	•	Trained on structured phishing dataset
	•	Uses engineered features (SSL, URL structure, etc.)
	•	High accuracy (~94%)

V3 Model
	•	Trained on real-world URLs
	•	Uses:
	•	Domain age
	•	DNS (MX record)
	•	IP resolution
	•	Captures real-time domain behavior

---

## Hybrid Logic

The final prediction is based on:
	•	Model V2 output
	•	Model V3 output
	•	Heuristic scoring

This improves:
	•	🔥 Robustness
	•	🔥 Real-world detection capability
	•	🔥 Reduced false negatives

---

## Dataset

	•	Phishing URLs: PhishTank
	•	Safe URLs: curated trusted domains
	•	Balanced dataset (250 safe + 250 phishing)
   
---

## Key Learnings
	•	Handling unreliable real-world data (DNS/WHOIS failures)
	•	Building hybrid ML systems
	•	Combining static + dynamic features
	•	Designing scalable ML pipelines

---

## Future Improvements
	•	🌐 Web interface (Streamlit / Flask)
	•	📧 Email phishing detection
	•	🧾 Website content analysis (HTML/JS)
	•	🧩 Browser extension integration

---

## Author
Manas Pandey
