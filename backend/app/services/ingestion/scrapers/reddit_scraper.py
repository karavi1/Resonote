import requests
from datetime import datetime
from .base_scraper import BaseScraper

class RedditScraper(BaseScraper):
    def __init__(self, subreddit="news", max_count=5, headless=True):
        self.subreddit = subreddit
        self.max_count = max_count
        # BaseScraper expects a driver, but we won't use it here
        self.driver = None

    def fetch_headlines(self, max_count=None):
        count = max_count or self.max_count
        url = f"https://www.reddit.com/r/{self.subreddit}/top.json?limit={count}&t=day"
        headers = {"User-Agent": "Resonote/1.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        posts = data["data"]["children"]

        return [
            {
                "title": post["data"]["title"],
                "url": f"https://www.reddit.com{post['data']['permalink']}"
            }
            for post in posts
        ]
    
    def ingest(self):
        url = f"https://www.reddit.com/r/{self.subreddit}/top.json?limit={self.max_count}&t=day"
        headers = {"User-Agent": "Resonote/1.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        posts = response.json()["data"]["children"]

        results = []

        for post in posts:
            data = post["data"]
            title = data["title"]
            external_url = data.get("url_overridden_by_dest") or f"https://www.reddit.com{data['permalink']}"

            results.append({
                "title": title,
                "url": external_url,
                "content": "",  # Will be filled by fetch_article_content
                "source": "reddit",
                "timestamp": datetime.utcnow().isoformat()
            })

        return results


    def fetch_article_content(self, url):
        return f"(Full Reddit post is viewable at: {url})"

    def close(self):
        pass
