import pytest
from flask import Flask, jsonify
from app.routes.core_routes import core_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(core_bp, url_prefix="/api")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello(client):
    resp = client.get("/api/hello")
    assert resp.status_code == 200
    assert b"Hello from Resonote API" in resp.data

def test_api_root(client):
    resp = client.get("/api/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "message" in data
    assert "endpoints" in data

def test_list_articles(client, monkeypatch):
    def mock_list_articles(args):
        return jsonify([{"id": 1, "title": "Test Article"}])
    monkeypatch.setattr("app.routes.core_routes.list_articles", mock_list_articles)
    resp = client.get("/api/articles")
    assert resp.status_code == 200

def test_ingest_generic_source(client, monkeypatch):
    def mock_process_source(source):
        return jsonify({"status": "success", "source": source, "ingested": 1})
    monkeypatch.setattr("app.routes.core_routes.process_source", mock_process_source)
    resp = client.post("/api/ingest/sample_source")
    assert resp.status_code == 200

def test_get_all_tags(client, monkeypatch):
    def mock_get_all_tags():
        return jsonify({"tag": "science", "count": 5})
    monkeypatch.setattr("app.routes.core_routes.get_all_tags", mock_get_all_tags)
    resp = client.get("/api/tags")
    assert resp.status_code == 200

def test_mark_as_read(client, monkeypatch):
    def mock_mark_as_read(article_id):
        return jsonify({"message": f"Article {article_id} marked as read"}), 200
    monkeypatch.setattr("app.routes.core_routes.mark_as_read", mock_mark_as_read)
    resp = client.post("/api/articles/42/mark-read")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Article 42 marked as read"

def test_toggle_favorite(client, monkeypatch):
    def mock_toggle_favorite(article_id):
        return jsonify({"message": f"Article {article_id} favorite toggled"}), 200
    monkeypatch.setattr("app.routes.core_routes.toggle_favorite", mock_toggle_favorite)
    resp = client.post("/api/articles/42/favorite")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Article 42 favorite toggled"

def test_make_reflection(client, monkeypatch):
    def mock_make_reflection(data, article_id):
        return jsonify({"message": f"Reflection created for {article_id}"}), 201
    monkeypatch.setattr("app.routes.core_routes.make_reflection", mock_make_reflection)
    resp = client.post("/api/reflect/make/1", json={"content": "My reflection"})
    assert resp.status_code == 201
    assert "Reflection created" in resp.get_json()["message"]

def test_fetch_reflection(client, monkeypatch):
    def mock_fetch_reflection(article_id):
        return jsonify({"article_id": article_id, "content": "Reflected thoughts"}), 200
    monkeypatch.setattr("app.routes.core_routes.fetch_reflection", mock_fetch_reflection)
    resp = client.get("/api/reflect/fetch/1")
    assert resp.status_code == 200
    assert resp.get_json()["content"] == "Reflected thoughts"

def test_update_reflection(client, monkeypatch):
    def mock_update_reflection(data, article_id):
        return jsonify({"message": f"Reflection for {article_id} updated"}), 200
    monkeypatch.setattr("app.routes.core_routes.update_reflection", mock_update_reflection)
    resp = client.post("/api/reflect/update/1", json={"content": "Updated reflection"})
    assert resp.status_code == 200
    assert "updated" in resp.get_json()["message"]

def test_delete_reflection(client, monkeypatch):
    def mock_delete_reflection(article_id):
        return jsonify({"message": f"Reflection {article_id} deleted"}), 200
    monkeypatch.setattr("app.routes.core_routes.delete_reflection", mock_delete_reflection)
    resp = client.delete("/api/reflect/delete/1")
    assert resp.status_code == 200
    assert "deleted" in resp.get_json()["message"]