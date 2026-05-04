import re
from urllib.parse import urlparse


def extract_features(url):
    features = {}

    # Fix domain parsing
    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    # ----------------------------
    # CORE FEATURES
    # ----------------------------

    features['having_IP'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', domain) else 0

    features['URLURL_Length'] = len(url)

    shorteners = ["bit.ly", "tinyurl.com", "goo.gl", "t.co"]
    features['Shortining_Service'] = 1 if any(s in url for s in shorteners) else 0

    features['having_At_Symbol'] = 1 if "@" in url else 0

    features['double_slash_redirecting'] = 1 if "//" in url[7:] else 0

    features['Prefix_Suffix'] = 1 if "-" in domain else 0

    features['having_Sub_Domain'] = 1 if domain.count('.') > 1 else 0

    features['SSLfinal_State'] = 1 if url.startswith("https") else 0

    features['HTTPS_token'] = 1 if "https" in domain else 0

    features['Submitting_to_email'] = 1 if "mailto" in url else 0

    features['Abnormal_URL'] = 1 if "@" in url else 0

    features['Redirect'] = 1 if "//" in url[7:] else 0

    # ----------------------------
    # DEFAULT FEATURES
    # ----------------------------

    features['Google_Index'] = 0
    features['Links_pointing_to_page'] = 0
    features['Statistical_report'] = 0
    features['URL_of_Anchor'] = 0
    features['web_traffic'] = 0
    features['Links_in_tags'] = 0
    features['SFH'] = 0
    features['Request_URL'] = 0
    features['Domain_registeration_length'] = 0
    features['age_of_domain'] = 0
    features['Page_Rank'] = 0
    features['DNSRecord'] = 0

    return features