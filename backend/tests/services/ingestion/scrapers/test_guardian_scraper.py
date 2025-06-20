import os
import pytest
from unittest.mock import patch, MagicMock
from app.services.ingestion.scrapers.guardian_scraper import GuardianScraper

@pytest.fixture
def sample_guardian_response():
    return {
        "response": {
            "results": [
                {
                    "webTitle": "Title A",
                    "webUrl": "https://www.theguardian.com/world/2023/oct/12/example-article",
                    "fields": {
                        "byline": "Reporter A"
                    }
                },
                {
                    "webTitle": "Title B",
                    "webUrl": "https://www.theguardian.com/us-news/2023/oct/13/another-article",
                    "fields": {
                        "byline": "Reporter B"
                    }
                }
            ]
        }
    }

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_fetch_headlines_success(mock_get, sample_guardian_response):
    mock_response = MagicMock()
    mock_response.json.return_value = sample_guardian_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.fetch_headlines(max_count=2)

    assert len(results) == 2
    assert results[0]["title"] == "Title A"
    assert results[0]["author"] == "Reporter A"
    assert results[0]["source"] == "guardian"
    assert "world" in results[0]["tags"]
    assert results[1]["title"] == "Title B"

@patch.dict(os.environ, {}, clear=True)
def test_guardian_scraper_raises_if_no_api_key():
    with pytest.raises(ValueError, match="Missing GUARDIAN_API_KEY"):
        GuardianScraper()

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_ingest_uses_fetch_headlines(mock_get, sample_guardian_response):
    mock_response = MagicMock()
    mock_response.json.return_value = sample_guardian_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.ingest(max_count=2)
    assert isinstance(results, list)
    assert results[0]["title"] == "Title A"

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_fetch_headlines_empty_response(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": {"results": []}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.fetch_headlines()
    assert results == []

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_fetch_headlines_handles_missing_fields(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": {
            "results": [
                {
                    "webTitle": "No fields example",
                    "webUrl": "https://www.theguardian.com/missing-fields/article"
                }
            ]
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.fetch_headlines()
    assert results[0]["author"] is None
    assert isinstance(results[0]["tags"], list)

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_fetch_headlines_fallback_on_all_http_errors(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP error")
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.fetch_headlines()
    assert results == []
    assert mock_get.call_count == 3  # Ensure all fallback attempts were made

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_excludes_corrections_and_clarifications(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": {
            "results": [
                {
                    "webTitle": "Corrections and Clarifications",
                    "webUrl": "https://www.theguardian.com/media/2024/jan/01/corrections",
                    "fields": {
                        "byline": "Guardian Staff"
                    }
                }
            ]
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.fetch_headlines()
    assert results == []

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_excludes_subscription_only_articles(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": {
            "results": [
                {
                    "webTitle": "Exclusive Analysis",
                    "webUrl": "https://www.theguardian.com/business/2024/feb/14/exclusive-analysis",
                    "fields": {
                        "byline": "Columnist X",
                        "access": "subscription"
                    }
                }
            ]
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.fetch_headlines()
    assert results == []

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_excludes_not_accessible_for_free(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": {
            "results": [
                {
                    "webTitle": "Premium Insights",
                    "webUrl": "https://www.theguardian.com/tech/2024/feb/20/premium-insights",
                    "fields": {
                        "byline": "Editor Z",
                        "isAccessibleForFree": "false"
                    }
                }
            ]
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.fetch_headlines()
    assert results == []

@patch.dict(os.environ, {"GUARDIAN_API_KEY": "test-key"})
@patch("app.services.ingestion.scrapers.guardian_scraper.requests.get")
def test_deduplicates_duplicate_urls(mock_get):
    duplicate_article = {
        "webTitle": "Duplicate Article",
        "webUrl": "https://www.theguardian.com/world/duplicate-article",
        "fields": {
            "byline": "Same Author"
        }
    }

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": {
            "results": [duplicate_article]
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    scraper = GuardianScraper()
    results = scraper.fetch_headlines(max_count=3)

    assert len(results) == 1
    assert results[0]["title"] == "Duplicate Article"