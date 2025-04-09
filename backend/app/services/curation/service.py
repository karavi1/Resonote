from app.db.session import SessionLocal
from app.db.crud import save_curated_article
from app.services.curation.cleaner import clean_html
from app.services.curation.metadata import extract_metadata
from newspaper import Article

def curate_document(raw_html: str, source_url: str, source: str = "unknown", db=None) -> dict:

    cleaned_text = clean_html(raw_html)
    metadata = extract_metadata(cleaned_text, source_url)

    curated = {
        "content": cleaned_text,
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

def fetch_article_content(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except Exception as e:
        print(f"[warn] Couldn't fetch content for {url}: {e}")
        return f"(Full article viewable at: {url})"



if __name__ == "__main__":
    with open("sample_reads/stroke_gut.html", "r") as f:
        raw_html = f.read()

    curated = curate_document(raw_html, "https://newatlas.com/stroke/gut-microbiome-stroke/")