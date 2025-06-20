import praw, os
from .base_scraper import BaseScraper
from urllib.parse import urlparse

BLACKLISTED_SUBS = {"modsupport", "paidcontent"}
BLACKLISTED_PHRASES = {"[deleted]", "[removed]", "subscribe", "paywall"}

class RedditScraper(BaseScraper):
    def __init__(self, subreddit="news", max_count=5, headless=True, **kwargs):
        self.subreddit = subreddit
        self.max_count = max_count

        for k, v in kwargs.items():
            print(f"[RedditScraper] Unused param: {k} = {v}")

        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("USER_AGENT")

        if not all([client_id, client_secret, user_agent]):
            raise EnvironmentError("Missing Reddit API credentials in environment")

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def is_valid_post(self, post):
        subreddit = post.subreddit.display_name.lower()
        if subreddit in BLACKLISTED_SUBS:
            return False

        title = (post.title or "")
        body = getattr(post, "selftext", "")
        author = str(post.author) if post.author else "none"

        combined_text = f"{title} {body} {author}".lower()

        if any(phrase in combined_text for phrase in BLACKLISTED_PHRASES):
            return False

        return True

    def fetch_headlines(self, max_count=None):
        count = max_count or self.max_count
        time_filters = ["day", "week", "month"]

        results = []
        seen_urls = set()

        for tf in time_filters:
            try:
                raw_posts = self.reddit.subreddit(self.subreddit).top(limit=50, time_filter=tf)
            except Exception as e:
                print(f"[RedditScraper] Error during fetch ({tf}): {e}")
                continue

            for post in raw_posts:
                if post.is_self or not self.is_valid_post(post):
                    continue

                url = post.url
                if url in seen_urls:
                    continue

                path_parts = urlparse(url).path.strip("/").split("/")
                tags = [p for p in path_parts if p and len(p) < 20]

                results.append({
                    "title": post.title,
                    "url": url,
                    "author": str(post.author),
                    "tags": tags[:5],
                    "source": "reddit"
                })
                seen_urls.add(url)

                if len(results) >= count:
                    return results

        return results

    def ingest(self, max_count=None):
        return self.fetch_headlines(max_count=max_count)

    def close(self):
        pass