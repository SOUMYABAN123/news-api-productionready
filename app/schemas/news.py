from pydantic import BaseModel
from typing import List

class ClassifiedArticle(BaseModel):
    title: str
    url: str | None = None
    predicted_category: str

class ClassifiedNewsResponse(BaseModel):
    items: List[ClassifiedArticle]
