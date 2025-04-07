from sqlalchemy.orm import Session 
from sqlmodel import select, desc
from .model import Blogs, BlogImage
from .schema import CreateBlog, UpdateBlog
import uuid 
from datetime import datetime
from fastapi import UploadFile
import os
from typing import List

UPLOAD_FOLDER = "uploads/"

class BlogsService:
    def get_all_blogs(self, session: Session):
        statement = select(Blogs).order_by(desc(Blogs.created_at))
        result = session.execute(statement)
        return result.scalars().all()

    def get_singleBlog(self, blog_uid: uuid.UUID, session: Session):
        statement = select(Blogs).where(Blogs.uid == blog_uid.bytes)
        result = session.execute(statement)
        return result.scalar_one_or_none()

    def save_images(self, images_files: List[UploadFile]) -> List[str]:
        saved_paths = []
        for img in images_files:
            if img:
                file_extension = img.filename.split('.')[-1]
                file_name = f'{uuid.uuid4()}.{file_extension}'
                file_path = os.path.join(UPLOAD_FOLDER, file_name)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                with open(file_path, 'wb') as buffer:
                    buffer.write(img.file.read())
                saved_paths.append(file_path)
        return saved_paths

    def create_blog(self, blog_data: CreateBlog, images_file: List[UploadFile], session: Session):
        # Create the blog first
        new_blog = Blogs(
            title=blog_data.title,
            slug=blog_data.slug,
            content=blog_data.content,
            summary=blog_data.summary,
            keywords=blog_data.keywords,
            author=blog_data.author,
        )
        
        session.add(new_blog)
        session.commit()
        session.refresh(new_blog)

        # Now handle images if any
        if images_file:
            images_path = self.save_images(images_file)
            for img_path in images_path:
                blog_image = BlogImage(
                    image_url=img_path,
                    blog_uid=new_blog.uid
                )
                session.add(blog_image)
            session.commit()
            session.refresh(new_blog)
            

        return new_blog
    
def update_blog(self, blog_uid: uuid.UUID, blog_update_data: UpdateBlog, images_file: List[UploadFile], session: Session):
    blog = session.query(Blogs).filter(Blogs.uid == blog_uid.bytes).first()
    if not blog:
        return None

    # Update blog fields
    for attr in ['title', 'slug', 'content', 'summary', 'keywords', 'author']:
        setattr(blog, attr, getattr(blog_update_data, attr, getattr(blog, attr)))

    # Handle images
    if images_file:
        # Delete old images
        for img in blog.images:
            if os.path.exists(img.image_url):
                os.remove(img.image_url)
            session.delete(img)
        
        # Add new images
        images_path = self.save_images(images_file)
        for img_path in images_path:
            blog_image = BlogImage(
                image_url=img_path,
                blog_uid=blog.uid
            )
            session.add(blog_image)

    blog.updated_at = datetime.now()
    session.commit()
    session.refresh(blog)
    
    # Update image URLs to full URLs before returning
    for img in blog.images:
        img.image_url = f"https://api.toprateddesigner.com/{img.image_url}"
    
    return blog

    def delete_blog(self, blog_uid: uuid.UUID, session: Session):
        blog = session.query(Blogs).filter(Blogs.uid == blog_uid.bytes).first()
        if blog:
            # Delete associated images
            for img in blog.images:
                if os.path.exists(img.image_url):
                    os.remove(img.image_url)
                session.delete(img)
            
            session.delete(blog)
            session.commit()
            return True
        return False