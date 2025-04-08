from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import Optional, List

class PortfolioImageBase(BaseModel):
    image_url: str

class PortfolioImage(PortfolioImageBase):
    uid: uuid.UUID
    portfolio_uid: uuid.UUID

class PortfolioBase(BaseModel):
    type: str
    title: str
    desc: str
    tech: List[str] = Field(default_factory=list)

class Portfolio(PortfolioBase):
    uid: uuid.UUID
    images: List[PortfolioImage] = []
    created_at: datetime
    updated_at: datetime

class CreatePortfolio(PortfolioBase):
    pass 

class UpdatePortfolio(PortfolioBase):
    images: Optional[List[str]] = []
