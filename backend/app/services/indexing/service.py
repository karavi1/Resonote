from app.db.models import CuratedArticle, Tag
from app.db.session import SessionLocal
from collections import Counter
from flask import jsonify
from sqlalchemy.orm import joinedload
from app.services.common import normalize_tag_name
from app.schemas.article import CuratedArticleRead
from app.schemas.tag import TagCount

def list_articles(request_args, db=None):
    db = db or SessionLocal()
    try:
        query = db.query(CuratedArticle).options(joinedload(CuratedArticle.reflection))

        if source := request_args.get("source"):
            query = query.filter(CuratedArticle.source == source)
        if status := request_args.get("status"):
            query = query.filter(CuratedArticle.reading_status == status)
        if (favorite := request_args.get("favorite")) is not None:
            if favorite.lower() in ["true", "1"]:
                query = query.filter(CuratedArticle.favorite.is_(True))
            elif favorite.lower() in ["false", "0"]:
                query = query.filter(CuratedArticle.favorite.is_(False))
        if tag := request_args.get("tag"):
            query = query.filter(CuratedArticle.tags.any(Tag.name == normalize_tag_name(tag)))

        query = query.order_by(CuratedArticle.timestamp.desc())
        limit = int(request_args.get("limit", 25))
        offset = int(request_args.get("offset", 0))
        articles = query.offset(offset).limit(limit).all()

        return jsonify([CuratedArticleRead.model_validate(article).model_dump() for article in articles])
    finally:
        db.close()

def get_all_tags(db=None):
    db = db or SessionLocal()
    try:
        tags = db.query(Tag).all()
        tag_counts = [
            TagCount(tag=tag.name, count=len(tag.articles)).model_dump()
            for tag in sorted(tags, key=lambda t: -len(t.articles))
        ]
        return jsonify(tag_counts)
    finally:
        db.close()

def mark_as_read(article_id, db=None):
    db = db or SessionLocal()
    try:
        article = db.get(CuratedArticle, article_id)
        if not article:
            return jsonify({"error": "Article not found"}), 404

        article.reading_status = "read"
        db.commit()
        db.refresh(article)
        return jsonify({"message": "Article marked as read"})
    finally:
        db.close()

def toggle_favorite(article_id, db=None):
    db = db or SessionLocal()
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