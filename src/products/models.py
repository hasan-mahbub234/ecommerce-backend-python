from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
import uuid
from typing import List
from sqlalchemy import JSON, Text

class Products(SQLModel, table=True):
    __tablename__ = 'Products'

    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            nullable=False,
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )
    name: str = Field(nullable=False)
    price: int = Field(nullable=False)
    quantity: int = Field(nullable=False)
    image: str = Field(nullable=False)
    video: str = Field(nullable=False)  # New field for video URL/path
    description: str = Field(
        sa_column=Column(Text, nullable=False)  # ✅ Supports HTML content
    )
    category: List[str] = Field(
        sa_column=Column(JSON)  # ✅ Removed nullable=False to avoid RuntimeError
    )
    offer: int = Field(nullable=True)  # ✅ New field for offers
    created_at: datetime = Field(
        sa_column=Column(
            mysqldb.DATETIME,
            nullable=False,
            default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            mysqldb.DATETIME,
            nullable=False,
            default=datetime.now,
            onupdate=datetime.now  # Auto-update timestamp
        )
    )
