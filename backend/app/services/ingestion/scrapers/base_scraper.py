from abc import ABC, abstractmethod
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

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
        Return a structured list of ingested metadata for downstream use.
        Each article should include:
        - title
        - url
        - author (optional)
        - tags (optional)
        - source
        - timestamp
        """
        articles = self.fetch_headlines(max_count=max_count)
        output = []
        for a in articles:
            output.append({
                "title": a.get("title"),
                "url": a.get("url"),
                "author": a.get("author"),
                "tags": a.get("tags", []),
                "source": self.__class__.__name__.replace("Scraper", "").lower(),
                "timestamp": datetime.utcnow().isoformat()
            })
        return output

    def close(self):
        self.driver.quit()
