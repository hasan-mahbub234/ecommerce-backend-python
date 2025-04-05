from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional


class SubCategoryBase(BaseModel):
    name: str
    image: Optional[str] = None  # Store image as string (path)


class SubCategory(SubCategoryBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CreateSubCategory(SubCategoryBase):
    pass


class UpdateSubCategory(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None 

