from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime
from typing import Optional, List

class ProjectBase(BaseModel):
    name: str 
    desc: str 
    email: EmailStr 
    type: List[str] = Field(default_factory=list) 

class ProjectCreate(ProjectBase):
    pass

class Projects(ProjectBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[List[str]] = None