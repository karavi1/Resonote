from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class ScrapedArticle(BaseModel):
    title: str
    url: HttpUrl
    author: Optional[str] = None
    tags: List[str] = []
    source: str
    timestamp: datetime