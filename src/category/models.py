from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import JSON, String


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
    image: Optional[str] = Field(
        sa_column=Column(
            String(255),  # Store file path
            nullable=True, default= None
        )
    )
    sub_category: Optional[list] = Field(
        sa_column=Column(
            JSON,  # Use JSON column type for list of objects
            nullable=True
        )
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