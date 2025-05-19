from app.schemas.tag import TagCreate, TagRead

def test_tag_create():
    tag = TagCreate(name="science")
    assert tag.name == "science"

def test_tag_read():
    tag = TagRead(id=1, name="tech")
    assert tag.id == 1
    assert tag.name == "tech"