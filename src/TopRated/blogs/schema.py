from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional, List


# Blog Image Schemas
class BlogImageBase(BaseModel):
    image_url: str

class BlogImage(BlogImageBase):
    uid: uuid.UUID
    blog_uid: uuid.UUID


# Blog Schemas
class BlogsBase(BaseModel):
    title: str 
    slug: str 
    content: str 
    summary: str 
    keywords: str 
    author: str  


class Blogs(BlogsBase):
    uid: uuid.UUID
    images: List[BlogImage] = []
    created_at: datetime
    updated_at: datetime


class CreateBlog(BlogsBase):
    pass


class UpdateBlog(BlogsBase):
    images: Optional[List[str]] = []
