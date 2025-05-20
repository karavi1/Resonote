from abc import ABC, abstractmethod
from datetime import datetime, timezone
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from app.schemas.scraper import ScrapedArticle

class BaseScraper(ABC):
    def __init__(self, headless=True):
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(10)

    @abstractmethod
    def fetch_headlines(self, max_count=5):
        """
        Return a list of dicts with at least 'title' and 'url'.
        Optionally include 'author' and 'tags'.
        """
        pass

    def ingest(self, max_count=5):
        """
        Return a structured list of validated article metadata using ScrapedArticle schema.
        Each article includes:
        - title
        - url
        - author (optional)
        - tags (optional)
        - source
        - timestamp
        """
        raw_articles = self.fetch_headlines(max_count=max_count)
        validated = []

        for article in raw_articles:
            enriched = {
                "title": article.get("title"),
                "url": article.get("url"),
                "author": article.get("author"),
                "tags": article.get("tags", []),
                "source": self.__class__.__name__.replace("Scraper", "").lower(),
                "timestamp": datetime.now(timezone.utc)
            }
            validated.append(ScrapedArticle.model_validate(enriched).model_dump())

        return validated

    def close(self):
        self.driver.quit()