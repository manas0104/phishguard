import socket
import whois
import math
from collections import Counter
import dns.resolver
from urllib.parse import urlparse
from datetime import datetime
from difflib import SequenceMatcher
import warnings
import logging
import sys
import os
import json


# ----------------------------
# SUPPRESS WARNINGS / LOGS
# ----------------------------

# Suppress low-level socket errors
sys.stderr = open(os.devnull, 'w')

# Suppress warnings
warnings.filterwarnings("ignore")

# Suppress DNS + WHOIS logs
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
# LOAD BRAND LIST
# ----------------------------
def load_brands():
    try:
        with open("data/brands.txt", "r") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except:
        return []


# ----------------------------
# LOAD THREAT KEYWORDS
# ----------------------------
def load_threat_keywords():
    try:
        with open("data/threat_keywords.json", "r") as f:
            return json.load(f)
    except:
        return {}


# ----------------------------
# LOAD SUSPICIOUS TLDS
# ----------------------------
def load_suspicious_tlds():
    try:
        with open("data/suspicious_tlds.json", "r") as f:
            return json.load(f)
    except:
        return {}
    

# ----------------------------
# LOAD SUSPICIOUS ENCODINGS
# ----------------------------
def load_suspicious_encodings():
    try:
        with open("data/suspicious_encodings.json", "r") as f:
            return json.load(f)
    except:
        return {}


# ----------------------------
# LOAD SUSPICIOUS SUBDOMAINS
# ----------------------------
def load_suspicious_subdomains():
    try:
        with open("data/suspicious_subdomains.json", "r") as f:
            return json.load(f)
    except:
        return {}
    

# ----------------------------
# LOAD SUSPICIOUS PATHS
# ----------------------------
def load_suspicious_paths():
    try:
        with open("data/suspicious_paths.json", "r") as f:
            return json.load(f)
    except:
        return {}

# ----------------------------
# LOAD SUSPICIOUS QUERIES
# ----------------------------
def load_suspicious_queries():
    try:
        with open("data/suspicious_queries.json", "r") as f:
            return json.load(f)
    except:
        return {}


# ----------------------------
# LOAD CHARACTER REPLACEMENTS
# ----------------------------
def load_character_replacements():
    try:
        with open("data/character_replacements.json", "r") as f:
            return json.load(f)
    except:
        return {}


# ----------------------------
# NORMALIZE TEXT
# ----------------------------
def normalize_text(text):

    replacements = load_character_replacements()

    text = text.lower()

    for fake, real in replacements.items():
        text = text.replace(fake, real)

    return text


# ----------------------------
# CALCULATE TEXT SIMILARITY
# ----------------------------
def similarity(a, b):

    return SequenceMatcher(None, a, b).ratio()


# ----------------------------
# CALCULATE SHANNON ENTROPY
# ----------------------------
def calculate_entropy(text):

    if not text:
        return 0

    counter = Counter(text)

    length = len(text)

    entropy = 0

    for count in counter.values():

        probability = count / length

        entropy -= probability * math.log2(probability)

    return entropy

# ----------------------------
# GET DOMAIN FROM URL
# ----------------------------
def get_domain(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url

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

    if not url:
        url = ""

    features = {}

    normalized_url = normalize_text(url)


    # ----------------------------
    # TOKENIZED URL
    #----------------------------
    tokens = [
        token
        for token in normalized_url
            .replace(".", "-")
            .split("-")
        if token
    ]


    # ----------------------------
    # LOAD INTELLIGENCE DATA
    # ----------------------------
    brands = load_brands()

    threat_keywords = load_threat_keywords()

    suspicious_tlds = load_suspicious_tlds()

    suspicious_encodings = load_suspicious_encodings()

    suspicious_subdomains = load_suspicious_subdomains()

    suspicious_paths = load_suspicious_paths()

    suspicious_queries = load_suspicious_queries()

    # ----------------------------
    # BRAND DETECTION
    # ----------------------------
    features["has_brand_name"] = 1 if any(
        brand in normalized_url for brand in brands
    ) else 0


    # ----------------------------
    # TYPO SQUATTING SCORE
    # ----------------------------
    typo_score = 0

    raw_domain = get_domain(url) or url

    normalized_domain = (
        get_domain(normalized_url)
        or normalized_url
    )

    for brand in brands:

        similarity_score = similarity(
            brand,
            normalized_domain
        )

        if similarity_score > 0.7:

            # Detect spoofed variation
            if brand not in raw_domain.lower():
                typo_score += 1


    # ----------------------------
    # THREAT SCORE
    # ----------------------------
    threat_score = 0

    for keyword, weight in threat_keywords.items():

        if keyword in url.lower():
            threat_score += weight


    digit_count = sum(c.isdigit() for c in normalized_url)

    special_chars = sum(
        not c.isalnum()
        for c in normalized_url
    )


    # ----------------------------
    # ENCODED URL SCORE
    # ----------------------------
    encoded_url_score = 0

    for encoding, weight in suspicious_encodings.items():

        if encoding.lower() in url.lower():
            encoded_url_score += weight


    # ----------------------------
    # GET DOMAIN
    # ----------------------------
    domain = safe_call(get_domain, url)

    parsed_url = urlparse(url)

    path = parsed_url.path.lower()

    query = parsed_url.query.lower()


    # ----------------------------
    # EXTRACT TLD
    # ----------------------------
    tld = ""

    if domain and "." in domain:
        tld = "." + domain.split(".")[-1]
    

    # ----------------------------
    # SUBDOMAIN DEPTH
    # ----------------------------
    subdomain_depth = 0

    if domain:
        subdomain_depth = max(domain.count(".") - 1, 0)


    # ----------------------------
    # SUBDOMAIN RISK SCORE
    # ----------------------------
    subdomain_risk_score = 0

    subdomain_parts = domain.split(".") if domain else []

    for part in subdomain_parts:

        part = part.lower()

        if part in suspicious_subdomains:
            subdomain_risk_score += (
                suspicious_subdomains[part]
            )

    # Extra risk for excessive depth
    if subdomain_depth >= 3:
        subdomain_risk_score += subdomain_depth


    # ----------------------------
    # TLD RISK SCORE
    # ----------------------------
    tld_risk_score = suspicious_tlds.get(tld, 0)


    # ----------------------------
    # PATH DEPTH
    # ----------------------------
    path_depth = path.count("/")


    # ----------------------------
    # PATH RISK SCORE
    # ----------------------------
    path_risk_score = 0

    path_parts = path.split("/")

    for part in path_parts:

        part = part.strip().lower()

        if part in suspicious_paths:
            path_risk_score += suspicious_paths[part]


    # ----------------------------
    # QUERY PARAM COUNT
    # ----------------------------
    query_param_count = 0

    if query:
        query_param_count = query.count("&") + 1


    # ----------------------------
    # QUERY RISK SCORE
    # ----------------------------
    query_risk_score = 0

    for keyword, weight in suspicious_queries.items():

        if keyword in query:
            query_risk_score += weight


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
            "tld_risk_score": tld_risk_score,
            "num_dots": url.count('.'),
            "has_dash": 1 if "-" in url else 0,
            "encoded_url_score": encoded_url_score,
            "threat_score": threat_score,
            "typo_score": typo_score,
            "has_brand_name": features["has_brand_name"],
            "subdomain_depth": subdomain_depth,
            "subdomain_risk_score": subdomain_risk_score,
            "url_entropy": calculate_entropy(normalized_url),

            "token_count": len(tokens),

            "path_depth": path_depth,
            "path_risk_score": path_risk_score,

            "query_param_count": query_param_count,
            "query_risk_score": query_risk_score,

            "digit_ratio": (
                digit_count / max(len(normalized_url), 1)
            ),

            "special_char_ratio": (
                special_chars / max(len(normalized_url), 1)
            )
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
    # URL STRUCTURE FEATURES
    # ----------------------------
    features["url_length"] = len(url)

    features["num_dots"] = url.count('.')

    features["has_dash"] = 1 if "-" in url else 0


    # ----------------------------
    # URL ENTROPY
    # ----------------------------
    features["url_entropy"] = calculate_entropy(normalized_url)


    # ----------------------------
    # TOKEN COUNT
    # ----------------------------
    features["token_count"] = len(tokens)


    # ----------------------------
    # DIGIT RATIO
    # ----------------------------
    features["digit_ratio"] = (
        digit_count / max(len(normalized_url), 1)
    )

    # ----------------------------
    # SPECIAL CHARACTER RATIO
    # ----------------------------
    features["special_char_ratio"] = (
        special_chars / max(len(normalized_url), 1)
    )


    # ----------------------------
    # SEMANTIC THREAT FEATURE
    # ----------------------------
    features["threat_score"] = threat_score


    # ----------------------------
    # TYPO SQUATTING FEATURE
    # ----------------------------
    features["typo_score"] = typo_score


    # ----------------------------
    # TLD RISK FEATURE
    # ----------------------------
    features["tld_risk_score"] = tld_risk_score


    # ----------------------------
    # ENCODED URL FEATURE
    # ----------------------------
    features["encoded_url_score"] = encoded_url_score


    # ----------------------------
    # SUBDOMAIN FEATURES
    # ----------------------------
    features["subdomain_depth"] = subdomain_depth

    features["subdomain_risk_score"] = (
        subdomain_risk_score
    )


    # ----------------------------
    # PATH FEATURES
    # ----------------------------
    features["path_depth"] = path_depth

    features["path_risk_score"] = path_risk_score

    # ----------------------------
    # QUERY FEATURES
    # ----------------------------
    features["query_param_count"] = (
        query_param_count
    )

    features["query_risk_score"] = (
        query_risk_score
    )

    return features