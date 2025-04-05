from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List, Optional


class SubCategory(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None


class CategoryBase(BaseModel):
    name: str
    image: Optional[str] = None  # Store the file path or URL
    sub_category: Optional[List[SubCategory]] = None  # Use the SubCategory model


class Categories(CategoryBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CreateCategories(CategoryBase):
    pass  


class UpdateCategories(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    sub_category: Optional[List[SubCategory]] = None  
