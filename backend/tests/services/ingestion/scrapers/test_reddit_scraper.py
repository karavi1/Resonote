import os
import pytest
from unittest.mock import patch, MagicMock
from app.services.ingestion.scrapers.reddit_scraper import RedditScraper

@pytest.fixture
def mock_reddit_post():
    post = MagicMock()
    post.title = "Reddit Post Title"
    post.url = "https://www.reddit.com/r/news/comments/example-post"
    post.author = "reddituser"
    post.is_self = False
    return post

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_fetch_headlines_success(mock_praw, mock_reddit_post):
    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [mock_reddit_post]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines(max_count=1)

    assert len(results) == 1
    assert results[0]["title"] == "Reddit Post Title"
    assert results[0]["author"] == "reddituser"
    assert results[0]["source"] == "reddit"
    assert isinstance(results[0]["tags"], list)

@patch.dict(os.environ, {}, clear=True)
def test_reddit_scraper_raises_without_env():
    with pytest.raises(EnvironmentError, match="Missing Reddit API credentials"):
        RedditScraper()

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_ingest_delegates_to_fetch(mock_praw, mock_reddit_post):
    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [mock_reddit_post]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.ingest(max_count=1)
    assert len(results) == 1
    assert results[0]["title"] == "Reddit Post Title"

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_fetch_headlines_skips_self_posts(mock_praw):
    self_post = MagicMock()
    self_post.is_self = True
    self_post.title = "Self Post"
    self_post.url = "https://reddit.com"
    self_post.author = "user"

    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [self_post]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines(max_count=1)
    assert results == []

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_fetch_headlines_missing_author(mock_praw):
    post = MagicMock()
    post.title = "Post Without Author"
    post.url = "https://www.reddit.com/r/news/comments/example"
    post.author = None
    post.is_self = False

    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [post]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines(max_count=1)
    assert results[0]["author"] == "None"

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_fetch_headlines_empty_response(mock_praw):
    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = []
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines()
    assert results == []

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_fetch_headlines_handles_unexpected_structure(mock_praw):
    post = MagicMock()
    post.title = None
    post.url = "not-a-url"
    post.author = "testuser"
    post.is_self = False

    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [post]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines()
    assert results[0]["title"] is None
    assert results[0]["url"] == "not-a-url"
    assert isinstance(results[0]["tags"], list)

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_blacklisted_subreddit_is_skipped(mock_praw):
    post = MagicMock()
    post.title = "Legit Title"
    post.url = "https://example.com"
    post.author = "user"
    post.is_self = False
    post.subreddit.display_name = "modsupport"  # <- Blacklisted

    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [post]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines()
    assert results == []

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_blacklisted_phrase_in_title_skips_post(mock_praw):
    post = MagicMock()
    post.title = "You must subscribe to read this"
    post.url = "https://example.com"
    post.author = "validuser"
    post.is_self = False
    post.subreddit.display_name = "news"

    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [post]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines()
    assert results == []

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_blacklisted_author_skips_post(mock_praw):
    post = MagicMock()
    post.title = "Interesting Title"
    post.url = "https://example.com"
    post.author = "[deleted]"  # <- Blacklisted
    post.is_self = False
    post.subreddit.display_name = "news"

    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [post]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines()
    assert results == []

@patch.dict(os.environ, {
    "REDDIT_CLIENT_ID": "dummy_id",
    "REDDIT_CLIENT_SECRET": "dummy_secret",
    "USER_AGENT": "dummy_agent"
})
@patch("app.services.ingestion.scrapers.reddit_scraper.praw.Reddit")
def test_deduplicates_reddit_posts_by_url(mock_praw):
    post1 = MagicMock()
    post1.title = "Duplicate Post"
    post1.url = "https://www.reddit.com/r/news/comments/same"
    post1.author = "user1"
    post1.is_self = False
    post1.subreddit.display_name = "news"

    post2 = MagicMock()
    post2.title = "Duplicate Post Again"
    post2.url = post1.url  # Same URL
    post2.author = "user2"
    post2.is_self = False
    post2.subreddit.display_name = "news"

    mock_subreddit = MagicMock()
    mock_subreddit.top.return_value = [post1, post2]
    mock_praw.return_value.subreddit.return_value = mock_subreddit

    scraper = RedditScraper()
    results = scraper.fetch_headlines(max_count=2)

    assert len(results) == 1
    assert results[0]["url"] == post1.url