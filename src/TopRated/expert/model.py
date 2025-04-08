from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import JSON, Text, String

class Experts(SQLModel, table=True):
    __tablename__= 'Experts'

    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            nullable=False,
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )
    name: str = Field(nullable=False)
    type: str = Field(nullable=False)
    exp: str = Field(nullable=False)
    technology: List[str] = Field( 
        sa_column=Column(JSON),
        default=[],
    )
    image: str = Field(
        sa_column=Column(
            String(255),  # Store file path
            nullable=False
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