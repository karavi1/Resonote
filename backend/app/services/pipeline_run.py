from app.db.session import SessionLocal
from app.services.ingestion.service import ingest_from_source
from app.services.curation.service import curate_document, fetch_article_content

def process_source(source: str):
    articles = ingest_from_source(source, max_count=3)

    db = SessionLocal()
    try:
        for i, a in enumerate(articles):
            print(f"\n🔹 Article {i+1}: {a['title']}")
            full_article = fetch_article_content(a["url"])
            curated = curate_document(full_article, a["url"], source=a["source"], db=db)

            print("\n🧠 Metadata:")
            for k, v in curated["metadata"].items():
                print(f"{k}: {v}")

            print("\n📄 Content Preview:")
            print(curated["content"][:300])
            print("-" * 50)
    finally:
        db.close()

if __name__ == "__main__":
    process_source("reddit")