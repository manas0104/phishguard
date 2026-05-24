<div align="center">

# 🛡️ PhishGuard

### Hybrid AI-Powered Phishing Detection Engine

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-4.5-brightgreen?style=flat-square)](https://github.com/manas0104/phishguard)
[![Accuracy](https://img.shields.io/badge/Real--World%20Accuracy-92.5%25-orange?style=flat-square)](https://github.com/manas0104/phishguard)

*Combining static ML, real-time domain intelligence, adversarial training, and heuristic threat analysis to catch malicious URLs before they cause harm.*

</div>

---

## What is PhishGuard?

PhishGuard is a multi-layer phishing detection system that analyzes URLs using a **hybrid intelligence engine** — going far beyond basic ML classifiers. It fuses multiple detection strategies to produce a confident, explainable verdict on any URL.

```
$ python3 -m src.predict

Enter URL: paypal.login.verify.security-update.xyz

RESULT: ⚠️  Phishing Website
Confidence: 79.00%

--- Debug Info ---
V2 Probability:              0.70
V3 Probability:              0.00
Hybrid Intelligence Boost:   Activated
Final Risk Score:            0.79
```

```
$ python3 -m src.predict

Enter URL: https://github.com

RESULT: ✅ Legitimate Website
Confidence: 96.84%
```

---

## Architecture

```
                          ┌─────────────────────┐
                          │      Input URL      │
                          └──────────┬──────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
          ▼                          ▼                          ▼
┌──────────────────┐    ┌────────────────────┐    ┌────────────────────────┐
│  Static Features │    │ Real-Time Features │    │  Threat Intelligence   │
│    (Model V2)    │    │    (Model V3)      │    │      Databases         │
└────────┬─────────┘    └─────────┬──────────┘    └───────────┬────────────┘
         │                        │                           │
         ▼                        ▼                           ▼
┌──────────────────┐    ┌────────────────────┐    ┌────────────────────────┐
│ Random Forest V2 │    │ Random Forest V3   │    │   Heuristic Scoring    │
└────────┬─────────┘    └─────────┬──────────┘    └───────────┬────────────┘
         │                        │                           │
         └────────────────────────┼───────────────────────────┘
                                  ▼
                     ┌────────────────────────┐
                     │  Hybrid Decision Engine │
                     │  ─────────────────────  │
                     │  Weighted Fusion (0.7/0.3)│
                     │  Heuristic Boost Layer  │
                     └────────────┬───────────┘
                                  ▼
                     ┌────────────────────────┐
                     │   Final Risk Verdict   │
                     └────────────────────────┘
```

**Why two models?** V2 is fast and accurate on known phishing patterns. V3 catches brand-new domains with live intelligence. Together, they cover each other's blind spots.

---

## Detection Capabilities

### Model V2 — Static ML
Analyzes engineered URL features for rapid detection of known phishing structures:
- URL length, dot count, dash count
- Special characters and structural patterns
- SSL certificate presence

### Model V3 — Real-Time Domain Intelligence
Performs live feature extraction to catch newly registered phishing domains:
- WHOIS domain age
- DNS MX record analysis
- IP resolution
- Semantic URL analysis

### Threat Intelligence Layer
Seven cybersecurity intelligence databases work in parallel:

| Database | Purpose |
|---|---|
| `brands.txt` | Brand impersonation detection |
| `threat_keywords.json` | Phishing language patterns |
| `suspicious_tlds.json` | Risky TLD intelligence (`.xyz`, `.tk`, `.ru`, etc.) |
| `suspicious_subdomains.json` | Fake trust chain detection |
| `suspicious_paths.json` | Phishing workflow paths |
| `suspicious_queries.json` | Token and session abuse patterns |
| `character_replacements.json` | Homoglyph / typo-squatting attacks |
| `suspicious_encodings.json` | Encoded URL detection |

### Advanced Heuristics

**Typo-Squatting Detection** — Catches spoofed domains like `paypa1.com`, `g00gle-auth.xyz`, and `micr0soft-login.net` using character normalization and semantic similarity scoring.

**Entropy Analysis** — Calculates Shannon entropy to detect randomized/obfuscated phishing domains like `xj82kq-security-update-29.xyz`.

**Subdomain Abuse Detection** — Flags deep fake trust chains like `paypal.login.verify.security-update.xyz`.

**Encoded URL Detection** — Catches obfuscated phishing payloads using URL encoding (`%40`, `%2F`, `%3A`).

**Path & Query Threat Analysis** — Detects credential theft and session hijacking patterns in URL paths and query strings.

### Adversarial Training
V4.5 expanded training on adversarial phishing datasets covering:
- Encoded phishing URLs
- Cloud phishing attacks
- Crypto wallet scams
- MFA phishing workflows
- Deep subdomain abuse patterns
- Modern authentication scams

---

## Performance

| Model | Accuracy |
|---|---|
| V2 Static ML | ~94% (structured dataset) |
| V4.5 Hybrid Intelligence Engine | 92.5% (real-world generalization) |

> V4.5 trades a small amount of raw accuracy for dramatically improved resistance against adversarial attacks, encoded URLs, deep subdomain abuse, and modern phishing structures that static models miss entirely.

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
You'll be prompted to enter a URL. PhishGuard returns a verdict, confidence score, and full debug breakdown.

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
│   ├── url_dataset.csv               # V3 training dataset
│   ├── phishing.csv                  # V2 raw dataset
│   ├── adversarial_phishing_urls.txt # Adversarial training data
│   ├── brands.txt
│   ├── threat_keywords.json
│   ├── suspicious_tlds.json
│   ├── suspicious_subdomains.json
│   ├── suspicious_paths.json
│   ├── suspicious_queries.json
│   ├── suspicious_encodings.json
│   └── character_replacements.json
│
├── models/
│   ├── phish_model.pkl               # Trained V2 model
│   ├── features.pkl                  # V2 feature list
│   ├── phish_model_v3.pkl            # Trained V3 model
│   └── features_v3.pkl               # V3 feature list
│
├── src/
│   ├── predict.py                    # Main hybrid prediction entry point
│   ├── train_model.py                # V2 training script
│   ├── train_url_model.py            # V3 training script
│   ├── realtime_features.py          # Live WHOIS / DNS / IP extraction
│   ├── preprocess.py                 # Data cleaning and preprocessing
│   └── utils/
│       ├── feature_extraction.py     # Static feature engineering
│       └── load_data.py              # Dataset loader
│
├── Requirements.txt
└── README.md
```

---

## Version History

<details>
<summary><strong>V4.5 — Hybrid Intelligence Engine</strong> (Latest)</summary>

- Adversarial phishing dataset expansion
- Heuristic cybersecurity boosting engine
- Suspicious TLD intelligence
- Encoded URL detection
- Subdomain threat analysis
- Path and query risk analysis
- Enterprise-style hybrid scoring
</details>

<details>
<summary><strong>V4.4 — Structural Threat Analysis</strong></summary>

- Suspicious TLD scoring
- Encoded URL detection
- Subdomain analysis
- Path and query parameter intelligence
</details>

<details>
<summary><strong>V4.3 — Advanced URL Intelligence</strong></summary>

- Shannon entropy analysis
- Token and digit ratio analysis
- Special character ratio scoring
</details>

<details>
<summary><strong>V4.2 — Typo-Squatting Detection</strong></summary>

- Character normalization
- Homoglyph replacement detection
- Typo-squatting score (`typo_score`)
</details>

<details>
<summary><strong>V4.1 — Semantic Threat Intelligence</strong></summary>

- Phishing keyword analysis
- Brand impersonation detection
- Threat score (`threat_score`)
</details>

<details>
<summary><strong>V4.0 — Hybrid Detection Pipeline</strong></summary>

- Combined V2 and V3 into a unified pipeline
- Weighted score fusion (0.7 V2 / 0.3 V3)
- Reduced false positives on legitimate domains
</details>

<details>
<summary><strong>V3.0 – V1.0</strong></summary>

- **V3.0:** Live WHOIS, DNS, and IP resolution features
- **V2.0:** Random Forest on engineered URL features (~94% accuracy)
- **V1.0:** Rule-based heuristic prototype
</details>

---

## Roadmap

- [ ] Streamlit dashboard
- [ ] Browser extension integration
- [ ] Email phishing analysis
- [ ] HTML/JavaScript content scanning
- [ ] Real-time blacklist API integration
- [ ] Visual similarity detection
- [ ] LLM-assisted phishing explanation engine
- [ ] Threat feed synchronization

---

## Contributing

Contributions are welcome. You can help by:

- Improving detection accuracy
- Expanding threat intelligence databases
- Adding new phishing heuristics
- Contributing adversarial datasets
- Improving UI/UX or building the Streamlit dashboard

```bash
# Standard contribution workflow
git fork https://github.com/manas0104/phishguard
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a pull request
```

---

## Disclaimer

PhishGuard is developed for **cybersecurity education, phishing awareness, machine learning research, and defensive security experimentation**. It is not a replacement for enterprise-grade commercial security solutions.

---

<div align="center">

Made by [Manas Pandey](https://github.com/manas0104)

</div>
