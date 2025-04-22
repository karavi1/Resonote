from app.db.models import CuratedArticle, Reflection
from app.db.session import SessionLocal
from app.services.ingestion.scrapers.reuters_scraper import ReutersScraper
from app.services.ingestion.scrapers.reddit_scraper import RedditScraper
from collections import Counter
from flask import Blueprint, jsonify, request

#### TODO: EXPORT ALL OF THESE TO THE CORRESPONDING SERVICES FILES

#### TODO: RENAME THIS TO SOMETHING MORE MEANINGFUL
example_bp = Blueprint("example", __name__)

@example_bp.route("/", methods=["GET"])
def api_root():
    return jsonify({
        "message": "Welcome to the Resonote API!",
        "endpoints": [
            "/api/hello",
            "/api/articles",
            "/api/tags",
            "/api/reflect/<article_id>",
            "/api/articles/<article_id>/mark-read",
            "/api/articles/<article_id>/favorite",
            "/api/ingest/reuters",
            "/api/ingest/reddit"
        ]
    })

@example_bp.route("/hello")
def hello():
    return "Hello from blueprint!" # Access at http://localhost:5000/api/hello

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

@example_bp.route("/articles", methods=["GET"])
def list_articles():
    db = SessionLocal()
    try:
        query = db.query(CuratedArticle)

        # Filter: source
        source = request.args.get("source")
        if source:
            query = query.filter(CuratedArticle.source == source)

        # Filter: reading_status
        status = request.args.get("status")
        if status:
            query = query.filter(CuratedArticle.reading_status == status)

        # Filter: favorite (true/false)
        favorite = request.args.get("favorite")
        if favorite is not None:
            if favorite.lower() in ["true", "1"]:
                query = query.filter(CuratedArticle.favorite.is_(True))
            elif favorite.lower() in ["false", "0"]:
                query = query.filter(CuratedArticle.favorite.is_(False))

        # Filter: tag contains
        tag = request.args.get("tag")
        if tag:
            query = query.filter(CuratedArticle.tags.like(f"%{tag}%"))

        # Sorting and pagination
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
                "favorite": a.favorite,
                "timestamp": a.timestamp.isoformat()
            } for a in articles
        ])
    finally:
        db.close()


@example_bp.route("/tags", methods=["GET"])
def get_all_tags():
    db = SessionLocal()
    try:
        all_tags = []
        articles = db.query(CuratedArticle).all()
        for article in articles:
            if article.tags:
                all_tags.extend([tag.strip().lower() for tag in article.tags.split(",") if tag.strip()])

        tag_counts = Counter(all_tags)

        return jsonify([
            { "tag": tag, "count": count }
            for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1])
        ])
    finally:
        db.close()

@example_bp.route("/articles/<int:article_id>/mark-read", methods=["POST"])
def mark_as_read(article_id):
    db = SessionLocal()
    try:
        article = db.query(CuratedArticle).get(article_id)
        if not article:
            return jsonify({"error": "Article not found"}), 404

        article.reading_status = "read"
        db.commit()
        return jsonify({"message": "Article marked as read"})
    finally:
        db.close()

@example_bp.route("/articles/<int:article_id>/favorite", methods=["POST"])
def toggle_favorite(article_id):
    db = SessionLocal()
    try:
        article = db.query(CuratedArticle).filter(CuratedArticle.id == article_id).first()
        if not article:
            return jsonify({"error": "Article not found"}), 404
        new_value = not bool(article.favorite)
        setattr(article, 'favorite', new_value)
        db.add(article)
        db.commit()
        db.refresh(article)
        print(f"Favorite toggled: {article.id} → {article.favorite}")
        return jsonify({
            "message": "Favorite toggled",
            "favorite": article.favorite
        })
    finally:
        db.close()

@example_bp.route("/reflect/<int:article_id>", methods=["POST"])
def make_reflection(article_id):
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data or "content" not in data:
            return jsonify({"error": "Missing reflection content"}), 400

        content = data["content"]

        article = db.query(CuratedArticle).filter(CuratedArticle.id == article_id).first()
        if not article:
            return jsonify({"error": "Article not found"}), 404

        reflection = Reflection(
            article_id=article_id,
            content=content
        )

        db.add(reflection)
        db.commit()
        db.refresh(reflection)

        return jsonify({
            "message": "Reflection saved",
            "reflection_id": reflection.id,
            "article_title": article.title
        }), 201

    finally:
        db.close()
