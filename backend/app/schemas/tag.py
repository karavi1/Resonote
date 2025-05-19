from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: int

    model_config = {
        "from_attributes": True
    }