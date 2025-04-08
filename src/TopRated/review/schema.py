from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import Optional, List

class ReviewBase(BaseModel):
    name: str 
    review: str 
    position: str   
    image: Optional[str] = None 

class Review(ReviewBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

class CreateReview(ReviewBase):
    pass

class UpdateReview(BaseModel):
    name: Optional[str] = None
    review: Optional[str] = None 
    position: Optional[str] = None 
    image: Optional[str] = None