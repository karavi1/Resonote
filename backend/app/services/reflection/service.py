from app.db.models import CuratedArticle, Reflection
from app.db.session import SessionLocal
from flask import jsonify
from sqlalchemy.orm import joinedload

def make_reflection(data, article_id):
    db = SessionLocal()
    try:
        if not data or "content" not in data:
            return jsonify({"error": "Missing reflection content"}), 400
        content = data["content"]
        article = db.query(CuratedArticle).options(joinedload(CuratedArticle.reflection)).filter(CuratedArticle.id == article_id).first()
        if not article:
            return jsonify({"error": "Article not found"}), 404
        if article.reflection:
            db.delete(article.reflection)
            db.flush()
        reflection = Reflection(article_id=article_id, content=content)
        article.reflection = reflection
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

def fetch_reflection(article_id):
    db = SessionLocal()
    try:
        article = db.query(CuratedArticle).filter(CuratedArticle.id == article_id).first()
        if not article:
            return jsonify({"error": "Article not found"}), 404
        
        reflection = db.query(Reflection).filter(Reflection.article_id == article_id).first()
        if not reflection:
            return jsonify({"error": "Reflection not found"}), 404
        return jsonify({
            "reflection": reflection.content
        })
    finally:
        db.close()

def update_reflection(data, article_id):
    db = SessionLocal()
    try:
        if not data or "content" not in data:
            return jsonify({"error": "Missing reflection content"}), 400
        content = data["content"]
        article = db.query(CuratedArticle).filter(CuratedArticle.id == article_id).first()
        if not article:
            return jsonify({"error": "Article not found"}), 404

        existing_reflection = db.query(Reflection).filter(Reflection.article_id == article_id).first()
        if existing_reflection:
            db.delete(existing_reflection)
            db.commit()

        new_reflection = Reflection(article_id=article_id, content=content)
        db.add(new_reflection)
        db.commit()
        db.refresh(new_reflection)

        return jsonify({
            "message": "Reflection updated",
            "reflection_id": new_reflection.id,
            "article_title": article.title
        }), 201
    finally:
        db.close()

def delete_reflection(article_id):
    db = SessionLocal()
    try:
        article = db.query(CuratedArticle).filter(CuratedArticle.id == article_id).first()
        if not article:
            return jsonify({"error": "Article not found"}), 404
        article.reflection = None
        db.add(article)
        db.commit()
        db.refresh(article)
        return jsonify({
            "message": "Reflection deleted"
        }), 200
    finally:
        db.close()