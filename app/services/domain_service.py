import whois
from urllib.parse import urlparse
from datetime import datetime


class DomainService:

    @staticmethod
    def get_domain_age(url):
        try:
            domain = urlparse(url).netloc.split(":")[0]
            if domain.startswith("www."):
                domain = domain[4:]

            info = whois.whois(domain)
            creation_date = info.creation_date

            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if creation_date:
                return (datetime.now() - creation_date).days

            return None

        except:
            return None
