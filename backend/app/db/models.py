from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class CuratedArticle(Base):
    __tablename__ = "curated_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512))
    author = Column(String(256), nullable=True)
    url = Column(Text)
    url_hash = Column(String(64), unique=True)
    source = Column(String(100))
    tags = Column(String(512))
    estimated_reading_time_min = Column(Integer)
    reading_status = Column(String(50), default="unread")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)