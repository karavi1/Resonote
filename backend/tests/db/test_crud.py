import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import OperationalError

from app.db.crud import save_curated_article
from app.db.models import CuratedArticle, Tag

@pytest.fixture
def sample_article_data():
    return {
        "metadata": {
            "title": "Test Article",
            "author": "Author",
            "url": "http://example.com/article",
            "estimated_reading_time_min": 5,
            "tags": ["science", "health"],
            "source": "example",
            "reading_status": "unread"
        }
    }

def mock_tags(tag_names):
    # Each mock tag has a unique id and name, mimicking the real model
    return [
        MagicMock(spec=Tag, id=i, name=name, _sa_instance_state=MagicMock())
        for i, name in enumerate(tag_names, start=1)
    ]

def test_save_new_article_success(monkeypatch, sample_article_data):
    db = MagicMock()
    db.query().filter().first.return_value = None

    monkeypatch.setattr(
        "app.services.common.get_or_create_tags",
        lambda db, tags: mock_tags(tags)
    )

    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None

    result = save_curated_article(db, sample_article_data)
    assert result.title == "Test Article"
    db.add.assert_called_once()
    db.commit.assert_called_once()

def test_save_existing_article_skips_insert(monkeypatch, sample_article_data):
    db = MagicMock()
    existing_article = MagicMock()
    db.query().filter().first.return_value = existing_article

    result = save_curated_article(db, sample_article_data)
    assert result == existing_article
    db.add.assert_not_called()
    db.commit.assert_not_called()

def test_retry_once_on_operational_error(monkeypatch, sample_article_data):
    db = MagicMock()

    # First call raises error, second call returns None
    db.query().filter().first.side_effect = [OperationalError("locked", {}, None), None]

    monkeypatch.setattr(
        "app.services.common.get_or_create_tags",
        lambda db, tags: mock_tags(tags)
    )

    db.rollback.return_value = None
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None

    result = save_curated_article(db, sample_article_data, retries=2, delay=0)
    db.rollback.assert_called_once()
    db.commit.assert_called_once()
    assert result.title == "Test Article"

def test_raises_after_max_retries(monkeypatch, sample_article_data):
    db = MagicMock()
    db.query().filter().first.side_effect = OperationalError("locked", {}, None)

    monkeypatch.setattr(
        "app.services.common.get_or_create_tags",
        lambda db, tags: mock_tags(tags)
    )

    db.rollback.return_value = None

    with pytest.raises(Exception, match="Failed to insert article after"):
        save_curated_article(db, sample_article_data, retries=2, delay=0)
    assert db.rollback.call_count == 2