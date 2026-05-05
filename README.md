# PhishGuard

> AI-powered phishing detection — combining static ML, real-time domain intelligence, and rule-based heuristics to catch malicious URLs before they cause harm.

---

## What is PhishGuard?

PhishGuard is a hybrid machine learning system that analyzes a URL and tells you whether it's phishing or safe with a confidence score and debug breakdown.

It runs **two models in parallel**:
- **Model V2** - trained on engineered features (URL structure, SSL, domain patterns)
- **Model V3** - trained on real-world URLs using live domain data (WHOIS, DNS, IP resolution)

Both predictions are fused using weighted logic, then filtered through rule-based heuristics for a final verdict.

**Plain English:** You paste a URL, PhishGuard checks it from multiple angles, and gives you a clear answer with reasoning.

---

## Quick Example

```
$ python3 -m src.predict

Enter URL: http://secure-login.paypa1.com/verify

RESULT: Phishing Website
Confidence: 94.37%

--- Debug Info ---
V2 Prediction:    Phishing  (-1)
V3 Prediction:    Phishing  (-1)
Suspicion Score:  3
Final Score:      2.81
```

```
$ python3 -m src.predict

Enter URL: https://github.com

RESULT: Legitimate Website
Confidence: 97.10%

--- Debug Info ---
V2 Prediction:    Legitimate (1)
V3 Prediction:    Legitimate (1)
Suspicion Score:  0
Final Score:      0.12
```

> The confidence score reflects how certain the hybrid system is. The suspicion score counts how many heuristic rules were triggered.

---

## Features

| Feature | Description |
|---|---|
| Dual-model detection | V2 (static) + V3 (real-time) run in parallel |
| Hybrid decision logic | Weighted fusion (0.7 V2 / 0.3 V3) with rule-based override |
| Real-time domain intelligence | WHOIS age, DNS MX records, IP resolution |
| Confidence scoring | Know how certain each prediction is |
| Debug output | See exactly why a URL was flagged |

---

## How It Works

```
Input URL
    │
    ├──▶  V2 Feature Extraction  ──▶  Model V2  (Static ML, ~94% accuracy)
    │     [SSL, URL length, dots,
    │      subdomains, special chars]
    │
    ├──▶  V3 Feature Extraction  ──▶  Model V3  (Real-time ML)
    │     [Domain age, DNS/MX records,
    │      IP resolution, semantic URL]
    │
    └──▶  Hybrid Decision Engine
              │
              ├── Weighted Score Fusion (0.7 / 0.3)
              ├── Heuristic Rule Override
              └── Final Prediction + Confidence
```

**Why two models?** Static features are fast and accurate on known patterns. Real-time features catch brand-new phishing domains that haven't been seen before. Together, they cover each other's blind spots.

---

## Installation

```bash
git clone https://github.com/manas0104/phishguard.git
cd phishguard
pip install -r Requirements.txt
```

**Requirements:** Python 3.8+, internet connection (for real-time V3 feature extraction)

---

## Usage

### Run a prediction

```bash
python3 -m src.predict
```

You will be prompted to enter a URL. The system returns the verdict, confidence score, and debug breakdown.

### Retrain the models

```bash
# Retrain V2 (static model)
python3 -m src.train_model

# Retrain V3 (real-time model)
python3 -m src.train_url_model
```

---

## Project Structure

```
PhishGuard/
│
├── data/
│   ├── url_dataset.csv           # Training dataset for V3
│   ├── phishing_cleaned.csv      # Cleaned phishing data (reference)
│   └── phishing.csv              # Raw dataset for V2
│
├── models/
│   ├── phish_model.pkl           # Trained V2 model
│   ├── features.pkl              # V2 feature list
│   ├── phish_model_v3.pkl        # Trained V3 model
│   └── features_v3.pkl           # V3 feature list
│
├── src/
│   ├── predict.py                # Main prediction entry point (hybrid)
│   ├── train_model.py            # V2 training script
│   ├── train_url_model.py        # V3 training script
│   ├── realtime_features.py      # Live WHOIS / DNS / IP feature extraction
│   ├── preprocess.py             # Data cleaning and preprocessing
│   └── utils/
│       ├── feature_extraction.py # Static feature engineering
│       └── load_data.py          # Dataset loader
│
├── Requirements.txt
└── README.md
```

---

## Dataset

| Source | Type | Size |
|---|---|---|
| PhishTank | Phishing URLs | 250 samples |
| Curated trusted domains | Legitimate URLs | 250 samples |

The dataset is balanced (50/50) to avoid model bias. V3 was trained on `url_dataset.csv`, which includes real-world URLs with live-fetched domain features.

---

## Version History

### v4.0 - Hybrid Phishing Detection System *(latest)*
- Combined V2 (static) and V3 (real-time) into a unified hybrid pipeline
- Improved V3 with semantic URL feature engineering
- Weighted score fusion (0.7 V2 / 0.3 V3)
- Reduced false positives on legitimate domains
- Improved real-world detection accuracy

### v3.0 - Real-Time Domain Intelligence
- Introduced Model V3 trained on real-world URLs
- Added live WHOIS, DNS (MX records), and IP resolution features
- V3 captures brand-new phishing domains not present in static datasets

### v2.0 - Static ML Detection
- Core ML model trained on engineered URL and SSL features
- ~94% accuracy on structured phishing dataset
- Features: URL length, subdomain depth, special characters, SSL validity, dot count

### v1.0 - Rule-Based Prototype
- Initial heuristic-only detection
- Keyword and pattern matching against known phishing indicators

---

## Roadmap

- [ ] Web interface (Streamlit or Flask)
- [ ] Email phishing detection
- [ ] HTML/JS content analysis
- [ ] Browser extension integration

---

## Author

**Manas Pandey** — [github.com/manas0104](https://github.com/manas0104)
