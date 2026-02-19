import re
from urllib.parse import urlparse


class FeatureExtractionService:

    @staticmethod
    def extract_features(url):

        parsed = urlparse(url)

        # 1️⃣ URL Length
        url_length = len(url)

        # 2️⃣ Number of digits
        num_digits = sum(c.isdigit() for c in url)

        # 3️⃣ Number of special characters
        special_chars = "!@#$%^&*()_+-=[]{}|;:'\",.<>/?"
        num_special = sum(c in special_chars for c in url)

        # 4️⃣ HTTPS flag
        has_https = 1 if parsed.scheme == "https" else 0

        # 5️⃣ IP address flag
        has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', parsed.netloc) else 0

        # 6️⃣ Number of subdomains
        num_subdomains = parsed.netloc.count('.') - 1 if '.' in parsed.netloc else 0

        # 7️⃣ Suspicious keywords
        suspicious_keywords = [
            "login", "verify", "update",
            "secure", "account", "bank",
            "signin", "confirm"
        ]

        contains_suspicious = 1 if any(word in url.lower() for word in suspicious_keywords) else 0

        return [
            url_length,
            num_digits,
            num_special,
            has_https,
            has_ip,
            num_subdomains,
            contains_suspicious
        ]
