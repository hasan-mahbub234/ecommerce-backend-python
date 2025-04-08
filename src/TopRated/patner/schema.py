from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import Optional, List

class PatnerBase(BaseModel):
    logo: Optional[str] = None
    name: str

class Patners(PatnerBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

class PatnerCreate(PatnerBase):
    pass 

class PatnerUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None