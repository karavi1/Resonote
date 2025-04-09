from app.services.ingestion.scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import time

class ReutersScraper(BaseScraper):
    def fetch_headlines(self, max_count=5):
        self.driver.get("https://www.reuters.com/")
        time.sleep(2)  # allow JS to load
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        articles = soup.select('a[data-testid="Heading"]')

        results = []
        for a in articles[:max_count]:
            title = a.get_text(strip=True)
            href = a.get("href")
            url = f"https://www.reuters.com{href}" if href.startswith("/") else href
            results.append({"title": title, "url": url})
        return results

    def fetch_article_content(self, url):
        self.driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        paragraphs = soup.select("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return content[:1000] + "..." if len(content) > 1000 else content