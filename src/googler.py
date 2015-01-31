import requests
import json


class Googler(object):

    GOOGLE_API_URL = "http://ajax.googleapis.com/ajax/services/search/web"
    GOOGLE_API_URL_VERSION = "1.0"

    def __init__(self, exclusions=[]):
        default_exclusions = [
            "setlist.fm",
            "ticketmaster.com",
            "songkick.com",
            "jambase.com",
            "facebook.com",
            "accessatlanta.com"
        ]
        self.exclusions = exclusions + default_exclusions

    def google(self, query):
        payload = {
            'q': self.build_query(query),
            'v': self.GOOGLE_API_URL_VERSION
        }

        resp = requests.get(self.GOOGLE_API_URL, params=payload)
        return json.loads(resp.text).get("responseData", {}).get("results", {})

    def google_concert_reviews_urls(self, query):
        results = self.google(query)
        return [r['url'] for r in results]

    def build_query(self, query):
        return query + " " + " ".join(self.build_exclusions())

    def build_exclusions(self):
        return [("-" + e) for e in self.exclusions]
