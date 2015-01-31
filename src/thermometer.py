import requests
import time
from bs4 import BeautifulSoup

import db
from db import Session, Review
from extractor import Extractor
from googler import Googler


class Thermometer(object):

    def __init__(self):
        artists = open('../lib/performers.csv', 'r').readlines()
        self.artists = artists[0].split(',')
        self.googler = Googler()
        self.extractor = Extractor()
        self.session = Session()

    def extract_all_reviews(self):
        for a in self.artists:
            self.extract_concert_reviews_for_performer(a)

    def extract_concert_reviews_for_performer(self, performer):
        existing = db.get_review_by_teamband_name(self.session, performer)
        if existing.count() >= 2:
            print performer + " was already in the database"
            return

        print "now scraping " + performer

        urls = self.googler.google_concert_reviews_urls(
            performer + " concert reviews")

        for url in urls[:2]:
            if db.get_review_by_url(self.session, url).count() != 0:
                continue
            response = requests.get(url)
            tree = BeautifulSoup(response.text)
            most_likey_review = self.extractor.extract(tree)

            r = Review(teamband_name=performer,
                       url=url,
                       review=most_likey_review)
            self.session.add(r)
            self.session.commit()

            time.sleep(10)

t = Thermometer()
t.extract_all_reviews()
