from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.schemas.tag import TagRead
from app.schemas.reflection import ReflectionRead

class CuratedArticleBase(BaseModel):
    title: str
    author: Optional[str]
    url: str
    source: str
    estimated_reading_time_min: int
    reading_status: str = "unread"
    favorite: bool = False

    model_config = {
        "extra": "forbid"
    }

class CuratedArticleCreate(CuratedArticleBase):
    tags: Optional[List[str]] = []

class CuratedArticleRead(CuratedArticleBase):
    id: int
    timestamp: datetime
    tags: List[TagRead] = []
    reflection: Optional[ReflectionRead] = None

    model_config = {
        "from_attributes": True,
        "extra": "forbid"
    }