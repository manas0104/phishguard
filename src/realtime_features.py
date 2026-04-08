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
        parsed = urlparse(url)
        return parsed.netloc
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

    if not domain:
        return {
            "domain_age": -1,
            "has_mx": 0,
            "has_ip": 0
        }

    age = safe_call(get_domain_age, domain)
    mx = safe_call(has_mx_record, domain)
    ip = safe_call(get_ip, domain)

    features["domain_age"] = age if age is not None else -1
    features["has_mx"] = 1 if mx else 0
    features["has_ip"] = 1 if ip else 0

    return features