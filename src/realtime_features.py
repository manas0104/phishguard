import socket
import whois
import dns.resolver
from urllib.parse import urlparse
from datetime import datetime
import warnings
import logging
import warnings
import sys
import os

# Suppress low-level socket errors
sys.stderr = open(os.devnull, 'w')

# Suppress warnings
warnings.filterwarnings("ignore")

# Suppress DNS + socket logs
logging.getLogger("dns").setLevel(logging.CRITICAL)
logging.getLogger("whois").setLevel(logging.CRITICAL)

# ----------------------------
# SAFE CALL WRAPPER
# ----------------------------
def safe_call(func, *args):
    try:
        return func(*args)
    except:
        return None


# ----------------------------
# GET DOMAIN FROM URL
# ----------------------------

def get_domain(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url  # ✅ fix for raw domains

        parsed = urlparse(url)
        domain = parsed.netloc

        return domain if domain else None

    except:
        return None


# ----------------------------
# GET DOMAIN AGE
# ----------------------------
def get_domain_age(domain):
    try:
        w = whois.whois(domain)

        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if not creation_date:
            return -1

        age = (datetime.now() - creation_date).days // 365
        return age

    except:
        return -1


# ----------------------------
# CHECK MX RECORD
# ----------------------------
def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return 1 if answers else 0
    except:
        return 0


# ----------------------------
# GET IP ADDRESS
# ----------------------------
def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None


# ----------------------------
# MAIN FEATURE EXTRACTOR
# ----------------------------
def extract_realtime_features(url):
    features = {}

    domain = safe_call(get_domain, url)

    # ----------------------------
    # BASIC FALLBACK
    # ----------------------------
    if not domain:
        return {
            "domain_age": -1,
            "has_mx": 0,
            "has_ip": 0,
            "has_https": 1,
            "url_length": len(url),
            "num_dots": url.count('.'),
            "has_dash": 1 if "-" in url else 0,
            "has_suspicious_word": 0
        }

    # ----------------------------
    # NETWORK FEATURES
    # ----------------------------
    age = safe_call(get_domain_age, domain)
    mx = safe_call(has_mx_record, domain)
    ip = safe_call(get_ip, domain)

    features["domain_age"] = age if age is not None else -1
    features["has_mx"] = 1 if mx else 0
    features["has_ip"] = 1 if ip else 0
    features["has_https"] = 1 if url.startswith("https") else 0

    # ----------------------------
    # 🔥 NEW URL-SEMANTIC FEATURES
    # ----------------------------
    features["url_length"] = len(url)
    features["num_dots"] = url.count('.')
    features["has_dash"] = 1 if "-" in url else 0

    suspicious_words = ["login", "secure", "verify", "account", "update", "bank", "paypal"]
    features["has_suspicious_word"] = 1 if any(word in url.lower() for word in suspicious_words) else 0

    return features