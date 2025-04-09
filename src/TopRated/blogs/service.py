from sqlalchemy.orm import Session 
from sqlmodel import select, desc
from .model import Blogs, BlogImage
from .schema import CreateBlog, UpdateBlog
import uuid 
from datetime import datetime
from fastapi import UploadFile
import os
from typing import List, Optional
import cloudinary 
import cloudinary.uploader

cloudinary.config(
    cloud_name="ddacq5ltb",
    api_key="985616939343421",
    api_secret="oI07cgZ3rGa0VJ8DW354oQV013g"
)

BASE_URL = "https://api.toprateddesigner.com/"

class BlogsService:
    def get_all_blogs(self, session: Session):
        statement = select(Blogs).order_by(desc(Blogs.created_at))
        result = session.execute(statement)
        blogs = result.scalars().all()
        for blog in blogs:
            self.update_image_urls_with_host(blog)
        return blogs

    def get_singleBlog(self, blog_uid: uuid.UUID, session: Session):
        statement = select(Blogs).where(Blogs.uid == blog_uid.bytes)
        result = session.execute(statement)
        blog = result.scalar_one_or_none()
        if blog:
            self.update_image_urls_with_host(blog)
        return blog

    def save_images(self, images_files: List[UploadFile]) -> List[str]:
        """Save multiple images to Cloudinary and return URLs"""
        saved_urls = []
        for img in images_files:
            if img:
                try:
                    result = cloudinary.uploader.upload(
                        img.file,
                        folder="blog_images",
                        public_id=f"img_{uuid.uuid4().hex}",
                        resource_type="auto"
                    )
                    saved_urls.append(result['secure_url'])
                except Exception as e:
                    print(f"Error uploading image {img.filename}: {e}")
                    continue
        return saved_urls

    def create_blog(self, blog_data: CreateBlog, images_file: List[UploadFile], session: Session):
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

        self.update_image_urls_with_host(new_blog)
        return new_blog

    # service.py
    def update_blog(self, blog_uid: uuid.UUID, blog_update_data: UpdateBlog, session: Session, images_file: Optional[List[UploadFile]] = None ):
        blog = session.query(Blogs).filter(Blogs.uid == blog_uid.bytes).first()
        if not blog:
            return None

        # Update only the fields that are provided
        for attr in ['title', 'slug', 'content', 'summary', 'keywords', 'author']:
            new_value = getattr(blog_update_data, attr)
            if new_value is not None:
                setattr(blog, attr, new_value)

        # Only update images if new images are provided
        if images_file is not None:
            # Delete existing images and files
            for img in blog.images:
                if os.path.exists(img.image_url):
                    os.remove(img.image_url)
                session.delete(img)

            # Add new images if provided
            if images_file:
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

        self.update_image_urls_with_host(blog)
        return blog

    def delete_blog(self, blog_uid: uuid.UUID, session: Session):
        blog = session.query(Blogs).filter(Blogs.uid == blog_uid.bytes).first()
        if blog:
            for img in blog.images:
                if os.path.exists(img.image_url):
                    os.remove(img.image_url)
                session.delete(img)

            session.delete(blog)
            session.commit()
            return True
        return False

    def update_image_urls_with_host(self, blog: Blogs):
        if blog.images:
            for img in blog.images:
                if not img.image_url.startswith("http"):
                    img.image_url = f"{BASE_URL}{img.image_url}"
