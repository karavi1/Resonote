from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReflectionBase(BaseModel):
    content: str

class ReflectionCreate(ReflectionBase):
    pass

class ReflectionUpdate(ReflectionBase):
    pass

class ReflectionRead(ReflectionBase):
    id: int
    article_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }