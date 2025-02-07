from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List

class CategoriesBase(BaseModel):
    name: str
    quantity: int
    image: str
    description: str
    sub_category: List[str]  

class Categories(CategoriesBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

class CreateCategories(CategoriesBase):
    pass  

class UpdateCategories(CategoriesBase):
    pass 
