from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from .service import BlogsService
from .schema import CreateBlog, UpdateBlog, Blogs
from typing import List, Optional
import uuid
from fastapi.responses import FileResponse
import os

blog_router = APIRouter()
blog_service = BlogsService()

@blog_router.get("/", response_model=List[Blogs])
def all_blogs(session: Session = Depends(get_session)):
    blogs = blog_service.get_all_blogs(session)
    return blogs

@blog_router.post("/", response_model=Blogs, status_code=status.HTTP_201_CREATED)
def create_blog(
    title: str = Form(...),
    slug: str = Form(...),
    content: str = Form(...),
    summary: str = Form(...),
    keywords: str = Form(...),
    author: str = Form(...),
    images_files: List[UploadFile] = File([]),
    session: Session = Depends(get_session)
):
    blog_data = CreateBlog(
        title=title,
        slug=slug,
        content=content,
        summary=summary,
        keywords=keywords,
        author=author
    )
    new_blog = blog_service.create_blog(blog_data, images_files, session)
    if not new_blog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create blog"
        )
    return new_blog

@blog_router.get("/{blog_uid}", response_model=Blogs)
def single_blog(blog_uid: uuid.UUID, session: Session = Depends(get_session)):
    blog = blog_service.get_singleBlog(blog_uid, session)
    if blog:
        return blog
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Blog not found"
    )



# route.py
@blog_router.patch("/{blog_uid}", response_model=Blogs)
def update_blog(
    blog_uid: uuid.UUID,
    title: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    keywords: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    images_files: Optional[List[UploadFile]] = File(None),
    session: Session = Depends(get_session)
):
    blog_update_data = UpdateBlog(
        title=title,
        slug=slug,
        content=content,
        summary=summary,
        keywords=keywords,
        author=author
    )
    updated_blog = blog_service.update_blog(
        blog_uid, blog_update_data, images_files, session
    )
    if updated_blog:
        return updated_blog
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Blog not found"
    )

@blog_router.delete("/{blog_uid}")
def delete_blog(blog_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = blog_service.delete_blog(blog_uid, session)
    if deleted:
        return {"message": "Blog deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Blog not found"
    )