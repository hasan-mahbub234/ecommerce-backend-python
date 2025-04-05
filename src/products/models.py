from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import JSON, Text, String


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
    quantity: int = Field(nullable=False)
    brand: str = Field(nullable=False)
    price: int = Field(nullable=False)
    category: str = Field(nullable=False)
    description: str = Field(
        sa_column=Column(Text, nullable=False)  # ✅ Supports HTML content
    )
    image: Optional[str] = Field(
        sa_column=Column(
            String(255),  # Store file path
            nullable=True, default= None
        )
    )
    video: Optional[str] = Field(
        sa_column=Column(
            String(255),  # Store file path
            nullable=True, default= None
        )
    )
    discount: Optional[int] = Field(default=None)  # ✅ Optional discount
    
    age: Optional[str] = Field(default=None)  # ✅ Optional age range
    sub_category: Optional[str] = Field(default=None)
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
