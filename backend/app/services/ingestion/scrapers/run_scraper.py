from app.services.ingestion.scrapers.reddit_scraper import RedditScraper
import json

def run():
    scraper = RedditScraper(headless=True)
    try:
        print("\n🔍 Running Reddit Ingestion...\n")
        results = scraper.ingest(max_count=5)

        for i, article in enumerate(results):
            print(f"\n{i+1}. {article['title']}")
            print(f"URL: {article['url']}")
            print(f"Author: {article.get('author')}")
            print(f"Tags: {', '.join(article.get('tags', []))}")
            print(f"Source: {article['source']}")
            print(f"Timestamp: {article['timestamp']}")

        with open("reddit_output.json", "w") as f:
            json.dump(results, f, indent=2)

    finally:
        scraper.close()

if __name__ == "__main__":
    run()
