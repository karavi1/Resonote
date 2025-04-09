from flask import Blueprint, jsonify
try:
    from app.db.session import SessionLocal
    from app.db.models import CuratedArticle
    from app.services.ingestion.scrapers.reuters_scraper import ReutersScraper
    from app.services.ingestion.scrapers.reddit_scraper import RedditScraper
except Exception as e:
    print("Error importing ReutersScraper:", e)

print("Example routes loaded")

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
        articles = db.query(CuratedArticle).order_by(CuratedArticle.timestamp.desc()).all()
        return jsonify([
            {
                "id": a.id,
                "title": a.title,
                "url": a.url,
                "reading_status": a.reading_status,
                "tags": a.tags,
                "timestamp": a.timestamp.isoformat()
            } for a in articles
        ]) # Access at http://localhost:5000/api/articles
    finally:
        db.close()
