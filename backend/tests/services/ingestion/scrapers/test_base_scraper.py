import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from app.services.ingestion.scrapers.base_scraper import BaseScraper

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
    assert result[0]["title"] == "Article 1"
    assert result[0]["source"] == "dummy"  # from DummyScraper
    assert "timestamp" in result[0]
    assert result[1]["tags"] == []  # default fallback
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
    assert ts.endswith("+00:00")
