import re
from urllib.parse import urlparse

class URLIntelligenceService:

    @staticmethod
    def detect_url_type(url):
        url = url.lower()

        if any(word in url for word in ["bank", "upi", "account", "paypal"]):
            return "Banking"
        elif any(word in url for word in ["shop", "cart", "store", "amazon"]):
            return "E-commerce"
        elif any(word in url for word in ["login", "signin", "verify"]):
            return "Login Page"
        else:
            return "General Website"

    @staticmethod
    def get_additional_flags(url):
        parsed = urlparse(url)

        return {
            "ip_address_used": bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)),
            "too_many_subdomains": parsed.netloc.count('.') > 3,
            "suspicious_keywords": [
                word for word in ["verify", "secure", "update", "confirm"]
                if word in url.lower()
            ]
        }
