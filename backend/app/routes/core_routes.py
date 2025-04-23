from app.services.ingestion.service import scrape_reddit_news, process_source
from app.services.indexing.service import list_articles, get_all_tags, mark_as_read, toggle_favorite
from app.services.reflection.service import make_reflection, fetch_reflection, update_reflection
from flask import Blueprint, current_app, jsonify, request

core_bp = Blueprint("core", __name__)

# Routing Health Checks

@core_bp.route("/hello")
def hello():
    return "Hello from Resonote API Blueprint Routing!"

@core_bp.route("/", methods=["GET"])
def api_root():
    endpoints = []
    for rule in current_app.url_map.iter_rules():
        # Filter to show only routes under "/api" and skip static files
        if rule.rule.startswith("/api") and "static" not in rule.endpoint:
            endpoints.append({
                "path": rule.rule,
                "methods": list(rule.methods - {"HEAD", "OPTIONS"})
            })

    return jsonify({
        "message": "Welcome to the Resonote API!",
        "endpoints": endpoints
    })


# Scraping, Ingestion and Storage Endpoints

@core_bp.route("/scrape/redditnews", methods=["GET"])
def scrape_reddit_news_route():
    return scrape_reddit_news()

@core_bp.route("/ingest/redditnews", methods=["POST"])
def ingest_reddit_news_route():
    return process_source("reddit")


# Indexing Endpoints

@core_bp.route("/articles", methods=["GET"])
def list_articles_route():
    return list_articles(request.args)

@core_bp.route("/tags", methods=["GET"])
def get_all_tags_route():
    return get_all_tags()

@core_bp.route("/articles/<int:article_id>/mark-read", methods=["POST"])
def mark_as_read_route(article_id):
    return mark_as_read(article_id)

@core_bp.route("/articles/<int:article_id>/favorite", methods=["POST"])
def toggle_favorite_route(article_id):
    return toggle_favorite(article_id)


# Reflection Endpoints

@core_bp.route("/reflect/make/<int:article_id>", methods=["POST"])
def make_reflection_route(article_id):
    return make_reflection(request.get_json(), article_id)

@core_bp.route("/reflect/fetch/<int:article_id>", methods=["GET"])
def fetch_reflection_route(article_id):
    return fetch_reflection(article_id)

@core_bp.route("/reflect/update/<int:article_id>", methods=["POST"])
def update_reflection_route(article_id):
    return update_reflection(request.get_json(), article_id)