from sqlmodel import SQLModel, Field, Column
import uuid
from typing import Optional
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
from sqlalchemy import String


class SubCategories(SQLModel, table=True):
    __tablename__ = 'subcategories'

    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            nullable=False,
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )
    name: str = Field(nullable=False)

    # Store image path instead of BLOB
    image: Optional[str] = Field(
        sa_column=Column(
            String(255),  # Store file path
            nullable=True, default= None
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
