from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import JSON, Text, String

class Projects(SQLModel, table=True):
    __tablename__ = 'Projects'

    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )

    name: str = Field(sa_column=Column(String(255), nullable=False))
    desc: str = Field(sa_column=Column(Text, nullable=False))
    email: str = Field(sa_column=Column(String(255), nullable=False))  
    type: List[str] = Field(
        sa_column=Column(JSON),
        default=[]
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
            onupdate=datetime.now
        )
    )