from flask import Blueprint, jsonify, request
from app.db.session import SessionLocal
from app.db.models import CuratedArticle
from app.services.ingestion.scrapers.reuters_scraper import ReutersScraper
from app.services.ingestion.scrapers.reddit_scraper import RedditScraper

example_bp = Blueprint("example", __name__)

@example_bp.route("/ingest/reuters", methods=["GET"])
def ingest_reuters():
    scraper = ReutersScraper(headless=True)
    try:
        results = scraper.ingest(max_count=5)
        return jsonify(results) # Access at http://localhost:5000/api/ingest/reuters
    finally:
        scraper.close()

@example_bp.route("/ingest/reddit", methods=["GET"])
def ingest_reddit_news():
    scraper = RedditScraper(headless=True)
    try:
        results = scraper.ingest(max_count=5)
        return jsonify(results) # Access at http://localhost:5000/api/ingest/reddit
    finally:
        scraper.close()


@example_bp.route("/hello")
def hello():
    return "Hello from blueprint!" # Access at http://localhost:5000/api/hello

@example_bp.route("/articles", methods=["GET"])
def list_articles():
    db = SessionLocal()
    try:
        query = db.query(CuratedArticle)

        source = request.args.get("source")
        if source:
            query = query.filter(CuratedArticle.source == source)

        status = request.args.get("status")
        if status:
            query = query.filter(CuratedArticle.reading_status == status)

        query = query.order_by(CuratedArticle.timestamp.desc())

        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
        articles = query.offset(offset).limit(limit).all()

        return jsonify([
            {
                "id": a.id,
                "title": a.title,
                "url": a.url,
                "source": a.source,
                "reading_status": a.reading_status,
                "tags": a.tags,
                "timestamp": a.timestamp.isoformat()
            } for a in articles
        ]) # Access at http://localhost:5000/api/articles
    finally:
        db.close()
