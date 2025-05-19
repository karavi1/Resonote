from datetime import datetime, timezone
from app.schemas.reflection import ReflectionCreate, ReflectionRead

def test_reflection_create():
    ref = ReflectionCreate(content="Insightful thought.")
    assert ref.content == "Insightful thought."

def test_reflection_read():
    now = datetime.now(timezone.utc)
    ref = ReflectionRead(
        id=1,
        article_id=42,
        content="Nice one.",
        created_at=now,
        updated_at=now
    )
    assert ref.id == 1
    assert ref.article_id == 42
    assert ref.content == "Nice one."
    assert ref.created_at == now