from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.db.models import CuratedArticle
from app.services.common import get_or_create_tags
from hashlib import sha256
import time

def save_curated_article(db: Session, article_data: dict, retries=3, delay=0.5):
    url = article_data["metadata"]["source_url"]
    url_hash = sha256(url.encode()).hexdigest()
    for attempt in range(retries):
        try:
            existing = db.query(CuratedArticle).filter(CuratedArticle.url_hash == url_hash).first()
            if existing:
                return existing
            article = CuratedArticle(
                title=article_data["metadata"]["title"],
                author=article_data["metadata"].get("author"),
                url=url,
                url_hash=url_hash,
                source=article_data["metadata"].get("source", "unknown"),
                estimated_reading_time_min=article_data["metadata"]["estimated_reading_time_min"],
                reading_status=article_data["metadata"].get("reading_status", "unread"),
                tags=get_or_create_tags(db, article_data["metadata"].get("tags", []))
            )

            db.add(article)
            db.commit()
            db.refresh(article)
            return article

        except OperationalError:
            print(f"[retry {attempt+1}] DB locked for {url}, retrying in {delay}s...")
            db.rollback()
            time.sleep(delay)

    raise Exception(f"Failed to insert article after {retries} retries (still locked)")