import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from app.db.models import Base
from app.db.models import CuratedArticle, Tag
from app.db.session import SessionLocal, engine

def test_sessionlocal_instantiation():
    session = SessionLocal()
    assert session.bind == engine
    assert hasattr(session, "commit")
    assert hasattr(session, "query")
    session.close()

@pytest.fixture
def test_db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session
    session.close()
    clear_mappers()

def test_can_insert_article(test_db_session):
    article = CuratedArticle(
        title="Test",
        author="Kaushik",
        url="http://something.com",
        url_hash="abc123",
        source="test",
        estimated_reading_time_min=2,
        reading_status="unread",
        tags=[]
    )
    test_db_session.add(article)
    test_db_session.commit()

    found = test_db_session.query(CuratedArticle).filter_by(url_hash="abc123").first()
    assert found is not None
    assert found.title == "Test"
