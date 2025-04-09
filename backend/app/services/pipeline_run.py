from app.db.session import SessionLocal
from app.services.ingestion.service import ingest_from_source
from app.services.curation.service import curate_document


def process_source(source: str):
    articles = ingest_from_source(source, max_count=5)
    db = SessionLocal()

    try:
        for i, a in enumerate(articles):
            print(f"\nA. Article {i+1}: {a['title']}")

            curated = curate_document(
                source_url=a["url"],
                title=a["title"],
                author=a.get("author"),
                source=a["source"],
                db=db
            )

            if not curated:
                print("⚠️ Skipped (missing metadata)")
                continue

            print("\nB. Metadata:")
            for k, v in curated["metadata"].items():
                print(f"{k}: {v}")

    finally:
        db.close()


if __name__ == "__main__":
    process_source("reddit")
    process_source("reuters")