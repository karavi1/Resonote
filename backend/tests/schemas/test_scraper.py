import pytest
from datetime import datetime, timezone
from app.schemas.scraper import ScrapedArticle

def test_scraped_article_valid():
    article = ScrapedArticle(
        title="Sample Title",
        url="https://example.com/article",
        author="Author Name",
        tags=["news", "health"],
        source="guardian",
        timestamp=datetime.now(timezone.utc)
    )
    assert article.title == "Sample Title"
    assert "health" in article.tags

def test_scraped_article_missing_required_field():
    with pytest.raises(Exception):
        ScrapedArticle(
            url="https://example.com",
            source="guardian",
            timestamp=datetime.now(timezone.utc)
        )

def test_scraped_article_invalid_url():
    with pytest.raises(Exception):
        ScrapedArticle(
            title="Bad URL Test",
            url="not-a-valid-url",
            source="guardian",
            timestamp=datetime.now(timezone.utc)
        )