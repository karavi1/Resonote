import os
import requests
from urllib.parse import urlparse
from .base_scraper import BaseScraper

# Docs: https://open-platform.theguardian.com/documentation/
class GuardianScraper(BaseScraper):
    def __init__(self, section="news", query=None, max_count=5, **kwargs):
        self.api_key = os.getenv("GUARDIAN_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GUARDIAN_API_KEY in environment variables.")

        self.section = section
        self.query = query
        self.max_count = max_count

        for k, v in kwargs.items():
            print(f"[GuardianScraper] Unused param: {k} = {v}")

    def fetch_headlines(self, max_count=None):
        count = max_count or self.max_count
        endpoint = "https://content.guardianapis.com/search"
        params = {
            "api-key": self.api_key,
            "section": self.section,
            "page-size": count,
            "order-by": "newest",
            "show-fields": "all",
        }
        if self.query:
            params["q"] = self.query

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("response", {}).get("results", []):
            fields = item.get("fields", {})
            url = item.get("webUrl")
            path_parts = urlparse(url).path.strip("/").split("/")
            tags = [p for p in path_parts if p and len(p) < 20]

            results.append({
                "title": item.get("webTitle"),
                "url": url,
                "author": fields.get("byline"),
                "tags": tags[:5],
                "source": "guardian"
            })

        return results

    def ingest(self, max_count=None):
        return self.fetch_headlines(max_count=max_count)

    def close(self):
        pass
