import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.ingestion import service as ingestion_service
from app.schemas.article import CuratedArticleCreate


### SCRAPER TESTS

@patch.dict("app.services.ingestion.service.SCRAPER_CLASSES", clear=True)
def test_scrape_from_source_dispatches():
    mock_scraper_class = MagicMock()
    mock_scraper = MagicMock()
    mock_scraper.ingest.return_value = [
        {"title": "Reddit 1", "url": "https://reddit.com/1", "source": "reddit"}
    ]
    mock_scraper_class.return_value = mock_scraper

    ingestion_service.SCRAPER_CLASSES["reddit"] = mock_scraper_class

    result = ingestion_service.scrape_from_source("reddit", max_count=1)

    assert len(result) == 1
    mock_scraper_class.assert_called_once_with(max_count=1, headless=True)
    mock_scraper.ingest.assert_called_once_with(max_count=1)
    mock_scraper.close.assert_called_once()


def test_scrape_from_source_invalid():
    with pytest.raises(ValueError, match="Unknown source"):
        ingestion_service.scrape_from_source("invalid")


### METADATA EXTRACTION

def test_extract_metadata_url_only():
    url = "https://example.com/news/article-title-here"
    result = ingestion_service.extract_metadata(source_url=url)
    assert result["title"] == "Article Title Here"
    assert "news" in result["tags"]
    assert result["estimated_reading_time_min"] == 3


def test_extract_metadata_with_title():
    url = "https://example.com/2023/10/sample"
    result = ingestion_service.extract_metadata(source_url=url, title="Custom Title")
    assert result["title"] == "Custom Title"


### CURATION

@patch("app.services.ingestion.service.save_curated_article")
def test_curate_document(mock_save):
    mock_save.return_value = {
        "metadata": {
            "title": "Test Title",
            "author": "Author A",
            "url": "https://example.com/news/title",
            "estimated_reading_time_min": 3,
            "reading_status": "unread",
            "source": "example",
            "tags": ["news"],
            "favorite": False
        }
    }

    mock_db = MagicMock()
    result = ingestion_service.curate_document(
        source_url="https://example.com/news/title",
        title="Test Title",
        author="Author A",
        source="example",
        db=mock_db
    )

    assert result["metadata"]["title"] == "Test Title"
    assert result["metadata"]["author"] == "Author A"
    assert result["metadata"]["source"] == "example"


@patch("app.services.ingestion.service.save_curated_article")
def test_store_curated_document_calls_save(mock_save):
    doc = {
        "metadata": {
            "title": "Stored Article",
            "source": "example",
            "url": "https://example.com",
            "estimated_reading_time_min": 3,
            "reading_status": "unread",
            "tags": ["example"],
            "favorite": False
        }
    }
    ingestion_service.store_curated_document(doc)
    mock_save.assert_called_once()


### PROCESSING

@patch("app.services.ingestion.service.scrape_from_source")
@patch("app.services.ingestion.service.curate_document")
@patch("app.services.ingestion.service.save_curated_article")
def test_process_source_success(mock_save, mock_curate, mock_scrape):
    mock_scrape.return_value = [
        {"title": "Example", "url": "https://example.com", "source": "reddit"}
    ]

    mock_curate.return_value = {
        "metadata": {
            "title": "Example",
            "author": "Author A",
            "url": "https://example.com",
            "source": "reddit",
            "estimated_reading_time_min": 3,
            "reading_status": "unread",
            "tags": ["reddit"],
            "favorite": False
        }
    }

    mock_save.return_value = {
        "metadata": {
            "title": "Example",
            "author": "Author A",
            "url": "https://example.com",
            "estimated_reading_time_min": 3,
            "reading_status": "unread",
            "source": "reddit",
            "tags": ["reddit"],
            "favorite": False
        }
    }


    app = Flask(__name__)
    with app.test_request_context("/?max_count=1&headless=true"):
        response = ingestion_service.process_source("reddit")
        data = response.get_json()

    article = CuratedArticleCreate.model_validate(data["curated"][0])

    assert data["status"] == "success"
    assert data["source"] == "reddit"
    assert data["ingested"] == 1
    assert article.title == "Example"