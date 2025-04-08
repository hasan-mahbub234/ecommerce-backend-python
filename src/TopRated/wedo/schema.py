from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import Optional, List, Union

class WedoBase(BaseModel):
    title: str 
    desc: str 
    service: List[str] = Field(default_factory=list)  
    image: Optional[str] = None 

class Wedo(WedoBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

class CreateWedo(WedoBase):
    pass

class UpdateWedo(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None 
    service: Optional[List[str]] = None 
    image: Optional[str] = None