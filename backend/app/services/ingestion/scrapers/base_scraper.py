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
        """Return a list of dicts with at least 'title' and 'url'."""
        pass

    @abstractmethod
    def fetch_article_content(self, url):
        """Return the full content string from the given URL."""
        pass

    def ingest(self, max_count=5):
        """Return a structured list of ingested content for downstream use."""
        articles = self.fetch_headlines(max_count=max_count)
        output = []
        for a in articles:
            content = self.fetch_article_content(a['url'])
            output.append({
                "title": a['title'],
                "url": a['url'],
                "content": content,
                "source": self.__class__.__name__.replace("Scraper", ""),
                "timestamp": datetime.utcnow().isoformat()
            })
        return output

    def close(self):
        self.driver.quit()