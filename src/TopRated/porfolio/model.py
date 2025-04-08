from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import JSON, Text, String, ForeignKey

class Portfolios(SQLModel, table= True):
    __tablename__= 'Portfolios'
    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )

    type: str = Field(nullable=False)
    title: str = Field(nullable=False)
    desc : str = Field(nullable=False)
    tech: List[str] = Field(  
        sa_column=Column(JSON),
        default=[],
    )
    images: List["PortfolioImage"] = Relationship(back_populates="portfolio")

    created_at: datetime = Field(
        sa_column=Column(mysqldb.DATETIME, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(mysqldb.DATETIME, default=datetime.now, onupdate=datetime.now)
    )


class PortfolioImage(SQLModel, table=True):
    __tablename__ = "portfolio_images"

    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )
    image_url: str = Field(sa_column=Column(String(255)))
    portfolio_uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            ForeignKey("Portfolios.uid"),
            name="portfolio_uid"
        )
    )
    portfolio: Optional[Portfolios] = Relationship(back_populates="images")