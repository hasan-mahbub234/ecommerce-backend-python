from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import Optional, List, Union

class ExpertBase(BaseModel):
    name: str 
    type: str 
    exp: str 
    technology: List[str] = Field(default_factory=list)  
    image: Optional[str] = None 

class Expert(ExpertBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

class ExpertCreate(ExpertBase):
    pass

class ExpertUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None 
    exp: Optional[str] = None 
    technology: Optional[List[str]] = None 
    image: Optional[str] = None