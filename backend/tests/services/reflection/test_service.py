import pytest
from unittest.mock import MagicMock
from flask import Flask
from app.services.reflection.service import make_reflection, fetch_reflection, update_reflection, delete_reflection

@pytest.fixture(scope="session", autouse=True)
def app_context():
    app = Flask(__name__)
    ctx = app.app_context()
    ctx.push()
    yield
    ctx.pop()

class DummyColumn:
    def is_(self, val): return f"is_({val})"
    def desc(self): return "DESC"

class DummyArticle:
    id = 1
    title = "Mock Article"
    reflection = None

    reflection = None
    id = DummyColumn()

class DummyReflection:
    article_id = DummyColumn()
    id = DummyColumn()

    def __init__(self, article_id, content):
        self.id = 42
        self.article_id = article_id
        self.content = content

@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    monkeypatch.setattr("app.services.reflection.service.joinedload", lambda x: x)
    monkeypatch.setattr("app.services.reflection.service.CuratedArticle", DummyArticle)
    monkeypatch.setattr("app.services.reflection.service.Reflection", DummyReflection)

def test_make_reflection_success(monkeypatch):
    mock_article = DummyArticle()

    mock_db = MagicMock()
    mock_db.query.return_value.options.return_value.filter.return_value.first.return_value = mock_article
    mock_db.commit.return_value = None
    mock_db.flush.return_value = None
    mock_db.refresh.return_value = None

    monkeypatch.setattr("app.services.reflection.service.SessionLocal", lambda: mock_db)
    monkeypatch.setattr("app.services.reflection.service.Reflection", DummyReflection)

    data = {"content": "This is a reflection."}
    response, status = make_reflection(data, 1)
    assert status == 201
    assert response.get_json()["message"] == "Reflection saved"


def test_make_reflection_missing_content(monkeypatch):
    monkeypatch.setattr("app.services.reflection.service.SessionLocal", lambda: MagicMock())
    response, status = make_reflection({}, 1)
    assert status == 400
    assert response.get_json()["error"] == "Missing reflection content"


def test_fetch_reflection_success(monkeypatch):
    mock_reflection = DummyReflection(1, "A saved reflection.")
    mock_article = DummyArticle()

    mock_db = MagicMock()
    mock_db.query.return_value.filter.side_effect = [
        MagicMock(first=lambda: mock_article),
        MagicMock(first=lambda: mock_reflection)
    ]

    monkeypatch.setattr("app.services.reflection.service.SessionLocal", lambda: mock_db)

    response = fetch_reflection(1)
    assert response.get_json()["reflection"] == "A saved reflection."


def test_fetch_reflection_not_found(monkeypatch):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    monkeypatch.setattr("app.services.reflection.service.SessionLocal", lambda: mock_db)
    response, status = fetch_reflection(1)
    assert status == 404
    assert response.get_json()["error"] == "Article not found"


def test_update_reflection_success(monkeypatch):
    mock_article = DummyArticle()
    mock_existing = DummyReflection(1, "Old reflection")

    mock_db = MagicMock()
    mock_db.query.return_value.filter.side_effect = [
        MagicMock(first=lambda: mock_article),
        MagicMock(first=lambda: mock_existing)
    ]
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    monkeypatch.setattr("app.services.reflection.service.SessionLocal", lambda: mock_db)
    monkeypatch.setattr("app.services.reflection.service.Reflection", DummyReflection)

    data = {"content": "Updated reflection."}
    response, status = update_reflection(data, 1)
    assert status == 201
    assert response.get_json()["message"] == "Reflection updated"


def test_delete_reflection_success(monkeypatch):
    mock_article = DummyArticle()

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_article
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    monkeypatch.setattr("app.services.reflection.service.SessionLocal", lambda: mock_db)

    response, status = delete_reflection(1)
    assert status == 200
    assert response.get_json()["message"] == "Reflection deleted"


def test_delete_reflection_article_not_found(monkeypatch):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    monkeypatch.setattr("app.services.reflection.service.SessionLocal", lambda: mock_db)

    response, status = delete_reflection(99)
    assert status == 404
    assert response.get_json()["error"] == "Article not found"