from pydantic import BaseModel


class Tag(BaseModel):
    title: str
