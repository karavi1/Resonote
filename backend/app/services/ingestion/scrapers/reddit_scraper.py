import requests
from urllib.parse import urlparse
from datetime import datetime
from .base_scraper import BaseScraper

class RedditScraper(BaseScraper):
    def __init__(self, subreddit="news", max_count=5, headless=True):
        self.subreddit = subreddit
        self.max_count = max_count
        self.driver = None  # Not used

    def fetch_headlines(self, max_count=None):
        count = max_count or self.max_count
        url = f"https://www.reddit.com/r/{self.subreddit}/top.json?limit={count}&t=day"
        headers = {"User-Agent": "Resonote/1.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        posts = response.json()["data"]["children"]

        results = []
        for post in posts:
            data = post["data"]

            external_url = data.get("url_overridden_by_dest")
            if not external_url or "reddit.com" in external_url:
                continue  # Skip self posts or Reddit-hosted content

            title = data["title"]
            author = data["author"]

            # Derive tags from external URL path
            path_parts = urlparse(external_url).path.strip("/").split("/")
            tags = [p for p in path_parts if p and len(p) < 20]

            results.append({
                "title": title,
                "url": external_url,
                "author": author,
                "tags": tags[:5]  # Limit to 5 tags
            })

        return results

    def close(self):
        pass