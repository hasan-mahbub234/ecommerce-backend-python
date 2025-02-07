from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List

class ProductBase(BaseModel):
    name: str
    price: int
    quantity: int
    offer: int
    image: str
    video: str  # New field for video URL/path
    description: str
    category: List[str]  # Changed to List[str] for multiple categories

class Products(ProductBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

class CreateProduct(ProductBase):
    pass  # No need to redefine fields, inherits from ProductBase

class UpdateProduct(ProductBase):
    pass  # Inherits all fields from ProductBase
