from sqlmodel import SQLModel, Field, Column
import uuid
from typing import Optional
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
from sqlalchemy import String


class User(SQLModel, table= True):
    __tablename__ = "Users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            nullable=False,
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )
    name: str = Field(nullable=False)
    email = str = Field(
        sa_column=Column(
            String(255),  
            unique=True, nullable=False
        )
    )

    is_verified = bool = Field(nullable=False)

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

    def __repr__(self):
        return f'<User{self.name}>'

    
