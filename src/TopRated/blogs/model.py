from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.mysql as mysqldb
from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import JSON, Text, String, ForeignKey

class Blogs(SQLModel, table=True):
    __tablename__ = "Blogs"

    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )
    title: str = Field(nullable=False)
    slug: str = Field(nullable=False)
    content: str = Field(nullable=False)
    summary: str = Field(nullable=False)
    keywords: str = Field(nullable=False)
    author: str = Field(nullable=False)
    
    images: List["BlogImage"] = Relationship(back_populates="blog")

    created_at: datetime = Field(
        sa_column=Column(mysqldb.DATETIME, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(mysqldb.DATETIME, default=datetime.now, onupdate=datetime.now)
    )


class BlogImage(SQLModel, table=True):
    __tablename__ = "blog_images"

    uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            primary_key=True,
            default=lambda: uuid.uuid4().bytes
        )
    )
    image_url: str = Field(sa_column=Column(String(255)))
    blog_uid: uuid.UUID = Field(
        sa_column=Column(
            mysqldb.BINARY(16),
            ForeignKey("Blogs.uid")
        )
    )
    blog: Optional[Blogs] = Relationship(back_populates="images")