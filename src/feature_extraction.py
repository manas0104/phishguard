import re
from urllib.parse import urlparse


def extract_features(url):
    features = {}

    parsed = urlparse(url)
    domain = parsed.netloc

    # ----------------------------
    # CORE FEATURES
    # ----------------------------

    # IP address detection
    features['having_IP'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', domain) else 0

    # URL length
    features['URLURL_Length'] = len(url)

    # Shortening service
    features['Shortining_Service'] = 1 if "bit.ly" in url else 0

    # @ symbol
    features['having_At_Symbol'] = 1 if "@" in url else 0

    # Double slash redirect
    features['double_slash_redirecting'] = 1 if "//" in url[7:] else 0

    # Prefix-Suffix (-)
    features['Prefix_Suffix'] = 1 if "-" in domain else 0

    # Subdomain count
    features['having_Sub_Domain'] = 1 if domain.count('.') > 1 else 0

    # HTTPS
    features['SSLfinal_State'] = 1 if url.startswith("https") else 0

    # HTTPS token
    features['HTTPS_token'] = 1 if "https" in domain else 0

    # Email submission
    features['Submitting_to_email'] = 1 if "mailto" in url else 0

    # Abnormal URL
    features['Abnormal_URL'] = 1 if "@" in url else 0

    # Redirect
    features['Redirect'] = 1 if "//" in url[7:] else 0
    
    # ----------------------------
    # DEFAULT EXTRA FEATURES
    # ----------------------------
    features['Google_Index'] = 0
    features['Links_pointing_to_page'] = 0
    features['Statistical_report'] = 0
    features['URL_of_Anchor'] = 0
    features['web_traffic'] = 0
    features['Links_in_tags'] = 0
    features['SFH'] = 0
    features['Links_pointing_to_page'] = 0
    features['Request_URL'] = 0
    features['Domain_registeration_length'] = 0
    features['age_of_domain'] = 0
    features['Page_Rank'] = 0
    features['DNSRecord'] = 0
    return features