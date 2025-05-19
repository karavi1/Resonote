import pytest
from unittest.mock import MagicMock
from flask import Flask
from app.services.indexing import service as indexing_service

class DummyColumn:
    def is_(self, val):
        return f"is_({val})"

    def desc(self):
        return "DESC"

class DummyArticle:
    id = 1
    title = "Test Article"
    url = "http://example.com"
    source = "guardian"
    reading_status = "unread"
    estimated_reading_time_min = 4

    favorite = DummyColumn()
    reflection = None
    timestamp = DummyColumn()

    def __init__(self):
        self.timestamp = MagicMock()
        self.timestamp.isoformat.return_value = "2025-05-19T12:00:00Z"
        self.tags = []
        self.reflection = None
        self.favorite = False


@pytest.fixture(scope="session", autouse=True)
def app_context():
    app = Flask(__name__)
    ctx = app.app_context()
    ctx.push()
    yield
    ctx.pop()


@pytest.fixture(autouse=True)
def patch_models(monkeypatch):
    monkeypatch.setattr("app.services.indexing.service.CuratedArticle", DummyArticle)
    monkeypatch.setattr("app.services.indexing.service.joinedload", lambda x: x)

def test_list_articles(monkeypatch):
    mock_article = DummyArticle()

    tag1 = MagicMock()
    tag1.name = "science"
    tag2 = MagicMock()
    tag2.name = "health"
    mock_article.tags = [tag1, tag2]

    reflection = MagicMock()
    reflection.id = 42
    reflection.content = "A thoughtful note"
    mock_article.reflection = reflection

    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_query.options.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.offset.return_value.limit.return_value.all.return_value = [mock_article]

    args = {
        "source": "guardian",
        "limit": "10",
        "offset": "0",
        "favorite": "false",
        "status": "unread",
    }

    response = indexing_service.list_articles(args, db=mock_db)
    data = response.get_json()

    assert isinstance(data, list)
    assert data[0]["title"] == "Test Article"
    assert data[0]["tags"] == ["science", "health"]
    assert data[0]["reflection"]["content"] == "A thoughtful note"


def test_get_all_tags(monkeypatch):
    mock_tag1 = MagicMock()
    mock_tag1.name = "science"
    mock_tag1.articles = [MagicMock(), MagicMock()]  # 2 articles

    mock_tag2 = MagicMock()
    mock_tag2.name = "health"
    mock_tag2.articles = [MagicMock()]  # 1 article

    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = [mock_tag1, mock_tag2]

    response = indexing_service.get_all_tags(db=mock_db)
    data = response.get_json()

    assert len(data) == 2
    assert data[0]["tag"] == "science"
    assert data[0]["count"] == 2


def test_mark_as_read_success():
    mock_article = MagicMock()
    mock_article.reading_status = "unread"

    mock_db = MagicMock()
    mock_db.get.return_value = mock_article

    response = indexing_service.mark_as_read(1, db=mock_db)
    data = response.get_json()

    assert data["message"] == "Article marked as read"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_article)


def test_mark_as_read_not_found():
    mock_db = MagicMock()
    mock_db.get.return_value = None

    response, status = indexing_service.mark_as_read(999, db=mock_db)
    assert status == 404
    assert response.get_json()["error"] == "Article not found"


def test_toggle_favorite():
    mock_article = MagicMock()
    mock_article.favorite = False

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_article

    response = indexing_service.toggle_favorite(1, db=mock_db)
    data = response.get_json()

    assert data["message"] == "Favorite toggled"
    assert data["favorite"] is True
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_article)


def test_toggle_favorite_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response, status = indexing_service.toggle_favorite(999, db=mock_db)
    assert status == 404
    assert response.get_json()["error"] == "Article not found"