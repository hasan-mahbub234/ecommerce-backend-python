from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    quantity: int
    description: str
    price: int
    brand: str
    category: str
    image: Optional[str] = None
    sub_category: Optional[str] = None
    age: Optional[str] = None
    discount: Optional[int] = None
    video: Optional[str] = None

class Products(ProductBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

class CreateProduct(ProductBase):
    pass  

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    sub_category: Optional[str] = None
    age: Optional[str] = None
    discount: Optional[int] = None
    video: Optional[str] = None
