from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONNECTION_STRING = "mysql://root:X8P947J2mDYsQ3unUqu4@localhost/thermometer"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    teamband_name = Column(String)
    url = Column(String)
    review = Column(String)

engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(bind=engine)


def get_review_by_teamband_name(session, teamband_name):
    return session.query(Review).filter_by(
        teamband_name=teamband_name)

def get_review_by_url(session, url):
    return session.query(Review).filter_by(url=url)
