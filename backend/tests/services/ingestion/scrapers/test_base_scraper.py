import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from app.services.ingestion.scrapers.base_scraper import BaseScraper
from dateutil.parser import isoparse
from app.schemas.scraper import ScrapedArticle

class DummyScraper(BaseScraper):
    def __init__(self):
        self.driver = MagicMock()

    def fetch_headlines(self, max_count=5):
        return [
            {"title": "Article 1", "url": "http://example.com/1", "author": "Alice", "tags": ["tech"]},
            {"title": "Article 2", "url": "http://example.com/2"}
        ]

def test_ingest_metadata_structure():
    scraper = DummyScraper()
    result = scraper.ingest(max_count=2)

    assert len(result) == 2
    validated = [ScrapedArticle.model_validate(article) for article in result]
    
    assert validated[0].title == "Article 1"
    assert validated[0].source == "dummy"
    assert validated[1].tags == []

    scraper.close()

def test_close_driver(monkeypatch):
    scraper = DummyScraper()
    scraper.driver.quit = MagicMock()
    scraper.close()
    scraper.driver.quit.assert_called_once()

def test_ingest_timestamp_utc():
    scraper = DummyScraper()
    result = scraper.ingest(max_count=1)
    ts = result[0]["timestamp"]

    assert isinstance(ts, datetime)
    assert ts.tzinfo is not None
    assert ts.utcoffset().total_seconds() == 0

def test_scraped_article_timestamp_is_datetime():
    article = ScrapedArticle.model_validate({
        "title": "Test",
        "url": "http://example.com",
        "source": "reddit",
        "timestamp": datetime.now(timezone.utc)
    })
    assert isinstance(article.timestamp, datetime)
