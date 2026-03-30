import re
from urllib.parse import urlparse


def extract_features(url):
    features = []

    url = url.lower()
    parsed = urlparse(url)
    domain = parsed.netloc

    # 1. Having IP Address
    features.append(-1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 1)

    # 2. URL Length
    if len(url) < 54:
        features.append(1)
    elif 54 <= len(url) <= 75:
        features.append(0)
    else:
        features.append(-1)

    # 3. Shortening Service
    shorteners = r"bit\.ly|goo\.gl|tinyurl|t\.co|is\.gd|buff\.ly"
    features.append(-1 if re.search(shorteners, url) else 1)

    # 4. @ symbol
    features.append(-1 if "@" in url else 1)

    # 5. Double slash redirect
    features.append(-1 if "//" in url[7:] else 1)

    # 6. Prefix-Suffix (- in domain)
    features.append(-1 if "-" in domain else 1)

    # 7. Subdomain count
    dots = domain.count(".")
    if dots == 1:
        features.append(1)
    elif dots == 2:
        features.append(0)
    else:
        features.append(-1)

    # 8. HTTPS
    features.append(1 if url.startswith("https") else -1)

    # 9. HTTPS token in domain
    features.append(-1 if "https" in domain else 1)

    # 10. Abnormal URL
    features.append(-1 if domain not in url else 1)

    # ---------------- NEW STRONG FEATURES ---------------- #

    # 11. Suspicious keywords
    keywords = ["login", "secure", "verify", "account", "update", "bank", "paypal"]
    count = sum(1 for word in keywords if word in url)

    if count == 0:
        features.append(1)
    elif count == 1:
        features.append(0)
    else:
        features.append(-1)

    # 12. Brand impersonation
    brands = ["paypal", "google", "facebook", "amazon", "bank"]
    features.append(-1 if any(b in url for b in brands) else 1)

    # 13. Too many digits in URL
    digits = sum(c.isdigit() for c in url)
    features.append(-1 if digits > 5 else 1)

    # 14. URL has suspicious TLD
    suspicious_tlds = [".tk", ".ml", ".ga", ".cf"]
    features.append(-1 if any(tld in domain for tld in suspicious_tlds) else 1)

    # 15. Length of domain
    if len(domain) < 10:
        features.append(1)
    elif len(domain) <= 20:
        features.append(0)
    else:
        features.append(-1)

    # ----------------------------------------------------- #

    # Ensure total features = 30
    features += [0] * (30 - len(features))

    return features