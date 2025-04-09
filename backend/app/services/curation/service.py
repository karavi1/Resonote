from app.db.session import SessionLocal
from app.db.crud import save_curated_article
from app.services.curation.metadata import extract_metadata

def curate_document(source_url: str, title: str = None, author: str = None, source: str = "unknown", db=None) -> dict:
    metadata = extract_metadata(source_url=source_url, title=title)

    if author:
        metadata["author"] = author

    curated = {
        "metadata": {
            **metadata,
            "reading_status": "unread",
            "source": source
        }
    }
    if db:
        save_curated_article(db, curated)
    return curated


def store_curated_document(doc: dict):
    db = SessionLocal()
    try:
        save_curated_article(db, doc)
        print(f"[DB] Stored: {doc['metadata']['title']}")
    finally:
        db.close()
