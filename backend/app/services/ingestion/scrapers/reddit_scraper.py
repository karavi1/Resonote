import praw, os
from .base_scraper import BaseScraper
from urllib.parse import urlparse

# Docs: https://praw.readthedocs.io/en/stable/
class RedditScraper(BaseScraper):
    def __init__(self, subreddit="news", max_count=5, headless=True, **kwargs):
        self.subreddit = subreddit
        self.max_count = max_count

        for k, v in kwargs.items():
            print(f"[RedditScraper] Unused param: {k} = {v}")

        # if kwargs: # see if needed
        #     raise ValueError(f"Unused params in RedditScraper: {kwargs}")

        client_id=os.getenv("REDDIT_CLIENT_ID")
        client_secret=os.getenv("REDDIT_CLIENT_SECRET")
        user_agent=os.getenv("USER_AGENT")

        if not all([client_id, client_secret, user_agent]):
            raise EnvironmentError("Missing Reddit API credentials in environment")

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def fetch_headlines(self, max_count=None):
        count = max_count or self.max_count
        posts = self.reddit.subreddit(self.subreddit).top(limit=count, time_filter="day")

        results = []
        for post in posts:
            if post.is_self:
                continue

            url = post.url
            path_parts = urlparse(url).path.strip("/").split("/")
            tags = [p for p in path_parts if p and len(p) < 20]

            results.append({
                "title": post.title,
                "url": url,
                "author": str(post.author),
                "tags": tags[:5],
                "source": "reddit"
            })

        return results

    def ingest(self, max_count=None):
        return self.fetch_headlines(max_count=max_count)

    def close(self):
        pass