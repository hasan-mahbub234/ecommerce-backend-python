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

@blog_router.get("/image/{blog_uid}")
def get_blog_images(blog_uid: uuid.UUID, session: Session = Depends(get_session)):
    blog = blog_service.get_singleBlog(blog_uid, session)
    if not blog or not blog.images:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Images not found"
        )
    
    # For multiple images, you might want to return a list of FileResponses
    # Here we're just returning the first image as an example
    first_image = blog.images[0] if isinstance(blog.images, list) else blog.images
    image_path = first_image.image_url  # Get the actual path from BlogImage object
    
    if os.path.exists(image_path):
        # Get file extension for media type
        file_extension = os.path.splitext(image_path)[1].lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".tiff": "image/tiff",
            ".ico": "image/vnd.microsoft.icon",
            ".svg": "image/svg+xml"
        }
        media_type = media_types.get(file_extension, "application/octet-stream")
        
        return FileResponse(image_path, media_type=media_type)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Image file not found"
    )

@blog_router.patch("/{blog_uid}", response_model=Blogs)
def update_blog(
    blog_uid: uuid.UUID,
    title: str = Form(None),
    slug: str = Form(None),
    content: str = Form(None),
    summary: str = Form(None),
    keywords: str = Form(None),
    author: str = Form(None),
    images_files: List[UploadFile] = File([]),
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