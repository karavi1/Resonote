from datetime import datetime, timezone
from app.schemas.tag import TagRead
from app.schemas.article import CuratedArticleCreate, CuratedArticleRead
from app.schemas.reflection import ReflectionRead

def test_curated_article_create():
    article = CuratedArticleCreate(
        title="Test Title",
        author="Author A",
        url="http://example.com",
        source="guardian",
        estimated_reading_time_min=4,
        reading_status="unread",
        favorite=True,
        tags=["tech", "science"]
    )
    assert article.title == "Test Title"
    assert article.tags == ["tech", "science"]

def test_curated_article_read():
    tag = TagRead(id=1, name="science")
    reflection = ReflectionRead(
        id=1,
        article_id=2,
        content="This is a reflection.",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    article = CuratedArticleRead(
        id=2,
        title="Test Title",
        author=None,
        url="http://example.com",
        source="reddit",
        estimated_reading_time_min=5,
        reading_status="read",
        favorite=False,
        timestamp=datetime.now(timezone.utc),
        tags=[tag],
        reflection=reflection
    )
    assert article.title == "Test Title"
    assert article.tags[0].name == "science"
    assert article.reflection.content == "This is a reflection."