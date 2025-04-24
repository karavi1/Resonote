from app.db.models import CuratedArticle
from app.db.session import SessionLocal
from collections import Counter
from flask import jsonify

def list_articles(request_args):
    db = SessionLocal()
    try:
        query = db.query(CuratedArticle)

        source = request_args.get("source")
        if source:
            query = query.filter(CuratedArticle.source == source)

        status = request_args.get("status")
        if status:
            query = query.filter(CuratedArticle.reading_status == status)

        favorite = request_args.get("favorite")
        if favorite is not None:
            if favorite.lower() in ["true", "1"]:
                query = query.filter(CuratedArticle.favorite.is_(True))
            elif favorite.lower() in ["false", "0"]:
                query = query.filter(CuratedArticle.favorite.is_(False))

        tag = request_args.get("tag")
        if tag:
            query = query.filter(CuratedArticle.tags.like(f"%{tag}%"))

        query = query.order_by(CuratedArticle.timestamp.desc())
        limit = int(request_args.get("limit", 25))
        offset = int(request_args.get("offset", 0))
        articles = query.offset(offset).limit(limit).all()

        return jsonify([
            {
                "id": article.id,
                "title": article.title,
                "url": article.url,
                "source": article.source,
                "reading_status": article.reading_status,
                "tags": article.tags,
                "favorite": article.favorite,
                "timestamp": article.timestamp.isoformat(),
                "reflection": article.reflection,
                "estimated_reading_time": article.estimated_reading_time_min,
                "reflection": article.reflection.content if article.reflection else None
            } for article in articles
        ])
    finally:
        db.close()

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

def mark_as_read(article_id):
    db = SessionLocal()
    try:
        article = db.query(CuratedArticle).get(article_id)
        if not article:
            return jsonify({"error": "Article not found"}), 404

        article.reading_status = "read"
        db.commit()
        db.refresh(article)
        return jsonify({"message": "Article marked as read"})
    finally:
        db.close()

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