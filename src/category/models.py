from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
import uuid
from typing import List
from sqlalchemy import JSON, Text

class Categories(SQLModel, table=True):
    __tablename__ = 'Categories'

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
    image: str = Field(nullable=False)
    description: str = Field(
        sa_column=Column(Text, nullable=False)  # ✅ Supports HTML content
    )
    sub_category: List[str] = Field(
        sa_column=Column(JSON)  # ✅ Removed nullable=False to avoid RuntimeError
    )
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
