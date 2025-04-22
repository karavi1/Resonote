from app.db.models import CuratedArticle, Reflection
from app.db.session import SessionLocal
from flask import jsonify

def fetch_reflection(article):
    return

def fetch_latest_reflection():
    return

def make_reflection(data, article_id):
    db = SessionLocal()
    try:
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