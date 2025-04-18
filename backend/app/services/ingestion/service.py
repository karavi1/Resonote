from app.services.ingestion.scrapers.reuters_scraper import ReutersScraper
from app.services.ingestion.scrapers.reddit_scraper import RedditScraper

SCRAPER_CLASSES = {
    "reuters": ReutersScraper,
    "reddit": RedditScraper,
}

def ingest_from_source(source: str, max_count=5, headless=True) -> list[dict]:
    """
    Ingest articles from the given source using its scraper.
    Returns a list of dicts: title, url, author, tags, source, timestamp
    """
    if source not in SCRAPER_CLASSES:
        raise ValueError(f"Unknown source: {source}")
    
    scraper_class = SCRAPER_CLASSES[source]
    scraper = scraper_class(headless=headless)

    try:
        return scraper.ingest(max_count=max_count)
    finally:
        scraper.close()
