from app.db.session import SessionLocal
from app.db.crud import save_curated_article
from app.services.common import normalize_tag_name
from app.services.ingestion.scrapers.guardian_scraper import GuardianScraper
from app.services.ingestion.scrapers.reddit_scraper import RedditScraper
from app.schemas.article import CuratedArticleRead, CuratedArticleCreate
from flask import jsonify, request
from urllib.parse import urlparse
import re

### INGESTION

SCRAPER_CLASSES = {
    "reddit": RedditScraper,
    "guardian": GuardianScraper
}

def scrape_from_source(source: str, max_count=5, headless=True, **params) -> list[dict]:
    """
    Pull/scrape articles from the given source using its scraper.
    Returns a list of dicts: title, url, author, tags, source, timestamp
    """
    if source not in SCRAPER_CLASSES:
        raise ValueError(f"Unknown source: {source}")
    
    scraper_class = SCRAPER_CLASSES[source]
    scraper = scraper_class(max_count=max_count, headless=headless, **params)

    try:
        return scraper.ingest(max_count=max_count)
    finally:
        scraper.close()

### CURATION/STORAGE

def extract_metadata(source_url: str, title: str = None) -> dict:
    """
    Extract metadata from a URL and optional title. No content parsing.
    """
    parsed = urlparse(source_url)
    path_parts = [part for part in parsed.path.strip("/").split("/") if part]

    # Use provided title or generate from URL
    fallback_title = re.sub(r"[-_/]+", " ", path_parts[-1]).title() if path_parts else parsed.netloc
    final_title = title or fallback_title

    # Basic tag extraction from URL path
    tags = [normalize_tag_name(part) for part in path_parts if part.isalpha() and len(part) > 2]

    return {
        "title": final_title,
        "author": None,
        "estimated_reading_time_min": 3,  # Default value
        "tags": tags[:5],
        "url": source_url,
    }

def curate_document(source_url: str, title: str = None, author: str = None, source: str = "unknown", db=None) -> dict:
    metadata = extract_metadata(source_url=source_url, title=title)

    if author:
        metadata["author"] = author

    return {
        "metadata": {
            **metadata,
            "reading_status": "unread",
            "source": source
        }
    }

def process_source(source: str):
    max_count = request.args.get("max_count", default=5, type=int)
    headless = request.args.get("headless", default=True, type=lambda v: v.lower() != "false")
    params = dict(request.args)
    params.pop("max_count", None)
    params.pop("headless", None)

    articles = scrape_from_source(
        source,
        max_count=max_count,
        headless=headless,
        **params
    )
    db = SessionLocal()
    curated_docs = []

    try:
        for i, a in enumerate(articles):
            print(f"\nA. Article {i+1}: {a['title']}")

            doc = curate_document(
                source_url=a["url"],
                title=a["title"],
                author=a.get("author"),
                source=a["source"],
                db=db
            )

            if not doc:
                print("Skipped (missing metadata)")
                continue

            try:
                validated = CuratedArticleCreate.model_validate(doc["metadata"])
            except Exception as e:
                print(f"❌ Skipped article due to validation error: {e}")
                continue
            
            save_curated_article(db, doc)
            curated_docs.append(validated.model_dump())

            print("\nB. Metadata:")
            for k, v in validated.model_dump().items():
                print(f"{k}: {v}")

    finally:
        db.close()

    return jsonify({
        "status": "success",
        "source": source,
        "ingested": len(curated_docs),
        "curated": curated_docs,
    })


# Helper Methods

def store_curated_document(doc: dict):
    db = SessionLocal()
    try:
        save_curated_article(db, doc)
        print(f"[DB] Stored: {doc['metadata']['title']}")
    finally:
        db.close()
