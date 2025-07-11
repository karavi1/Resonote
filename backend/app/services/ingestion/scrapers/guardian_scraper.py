import os
import requests
import httpx
from urllib.parse import urlparse
from .base_scraper import BaseScraper
from concurrent.futures import ThreadPoolExecutor

EXCLUDED_TITLES = {"corrections and clarifications"}
EXCLUDED_ACCESS = {"subscription", "premium", "members"}

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

    def is_valid_article(self, title, fields):
        if not title:
            return False
        if title.lower().strip() in EXCLUDED_TITLES:
            return False

        access_type = fields.get("access", "").lower()
        if access_type in EXCLUDED_ACCESS:
            return False

        if fields.get("isAccessibleForFree") == "false":
            return False

        return True

    def fetch_headlines(self, max_count=None):
        count = max_count or self.max_count
        endpoint = "https://content.guardianapis.com/search"
        order_by_options = ["newest", "relevance", "oldest"]

        results = []
        seen_urls = set()

        for order_by in order_by_options:
            params = {
                "api-key": self.api_key,
                "section": self.section,
                "page-size": count,
                "order-by": order_by,
                "show-fields": "all",
            }
            if self.query:
                params["q"] = self.query

            try:
                response = requests.get(endpoint, params=params)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                print(f"[GuardianScraper] Error during fetch ({order_by}): {e}")
                continue

            for item in data.get("response", {}).get("results", []):
                title = item.get("webTitle")
                fields = item.get("fields", {})
                url = item.get("webUrl")

                if url in seen_urls:
                    continue
                if not self.is_valid_article(title, fields):
                    seen_urls.add(url)
                    continue

                path_parts = urlparse(url).path.strip("/").split("/")
                tags = [p for p in path_parts if p and len(p) < 20]

                results.append({
                    "title": title,
                    "url": url,
                    "author": fields.get("byline"),
                    "tags": tags[:5],
                    "source": "guardian"
                })
                seen_urls.add(url)

                if len(results) >= count:
                    return results

        return results

    def ingest(self, max_count=None):
        return self.fetch_headlines(max_count=max_count)

    def close(self):
        pass