
# PhishGuard – Phishing Website Detection System

## Overview
PhishGuard is a Machine Learning based system that detects whether a given URL is safe or phishing.

The project is built step by step in multiple versions to simulate real world ML system development and improvement.

---

## Version 2 Highlights
- Feature importance-based selection (top features chosen automatically)
- Improved preprocessing pipeline (cleaning, encoding, outlier handling)
- Aligned training & prediction pipeline (no feature mismatch)
- Stable and consistent predictions
- Improved model performance (~94% accuracy)

---

## Workflow

1. Load dataset  
2. Perform preprocessing:
   - Remove useless columns  
   - Handle missing values  
   - Remove duplicates  
   - Encode categorical data  
   - Handle outliers  
3. Split features and target  
4. Train Random Forest model  
5. Extract feature importance  
6. Select top features automatically  
7. Retrain model using selected features  
8. Save:
   - Trained model (phish_model.pkl)
   - Selected feature list (features.pkl)  
9. Take URL input and predict in real-time  

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib

---

## Project Structure

PhishGuard/
│
├── data/
│   └── phishing.csv
│
├── models/
│   ├── phish_model.pkl
│   └── features.pkl
│
├── src/
│   ├── load_data.py
│   ├── preprocess.py
│   ├── train_model.py
│   ├── feature_extraction.py
│   ├── predict.py
│   └── test.py
│
├── .gitignore
└── README.md

---

## ▶️ How to Run

1. Train Model: 
python3 src/train_model.py

2. Predict URL: 
python3 src/predict.py

---

## Example

Enter URL: http://google.com

RESULT: 
Safe Website  
Confidence: 86.00%

---

## Model Performance

- Accuracy: ~94%
- Balanced precision & recall
- Reduced overfitting using feature selection
- Stable predictions due to aligned feature pipeline

---

## Limitations (Version 2)

- Uses dataset-based features (not real-time data)
- Some features use default values during prediction
- Does not yet fetch live domain information

---

## Future Improvements (Next Versions)

- Real-time feature extraction (WHOIS, DNS, IP lookup)
- HTML & content-based analysis
- Deep Learning models
- API-based phishing detection
- Web interface (Flask / Streamlit)
- Visualization dashboard

---

## Author
Manas Pandey
