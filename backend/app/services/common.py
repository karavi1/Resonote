from sqlalchemy.exc import IntegrityError
from app.db.models import Tag

def normalize_tag_name(tag: str) -> str:
    return tag.strip().lower()

def get_or_create_tags(db, tag_names: list[str]) -> list[Tag]:
    tag_cache = {}
    tags = []
    for raw_name in tag_names:
        name = normalize_tag_name(raw_name)
        if name in tag_cache:
            tag = tag_cache[name]
        else:
            tag = db.query(Tag).filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.add(tag)
                try:
                    db.flush()
                except IntegrityError:
                    db.rollback()
                    tag = db.query(Tag).filter_by(name=name).first()
            tag_cache[name] = tag
        tags.append(tag)
    return tags
