from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlparse
from .base_scraper import BaseScraper

class ReutersScraper(BaseScraper):
    def __init__(self, headless=True, max_count=5):
        super().__init__(headless=headless)
        self.max_count = max_count

    def fetch_headlines(self, max_count=None):
        def is_valid_article_url(url: str) -> bool:
            return (
                url.startswith("https://www.reuters.com/")
                and url.count("/") > 4
                and url.endswith("/")
                and not any(url.rstrip("/").split("/")[-1] in s for s in [
                    "world", "science", "business", "lifestyle", "technology"
                ])
            )

        self.driver.get("https://www.reuters.com/")
        raw_links = self.driver.find_elements(By.CSS_SELECTOR, "a[data-testid='Heading']")

        print(f"🔎 Found {len(raw_links)} candidate links")
        articles = []
        seen = set()

        for link in raw_links:
            url = link.get_attribute("href")
            title = link.text.strip()

            if not url or url in seen:
                continue
            seen.add(url)

            if url.startswith("/"):
                url = "https://www.reuters.com" + url

            if is_valid_article_url(url) and title:
                # Extract tags from URL path
                path_parts = urlparse(url).path.strip("/").split("/")
                tags = [part for part in path_parts if part and len(part) < 20]

                articles.append({
                    "title": title,
                    "url": url,
                    "author": None,
                    "tags": tags[:5]
                })

            if len(articles) >= self.max_count:
                break

        return articles

    def close(self):
        try:
            self.driver.quit()
        except WebDriverException:
            pass
