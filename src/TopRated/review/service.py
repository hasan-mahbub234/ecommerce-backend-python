from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .model import Reviews
from .schema import CreateReview, UpdateReview
import uuid
from datetime import datetime
from fastapi import UploadFile
import os
from typing import Optional
from ..blogs.service import BASE_URL
import cloudinary 
import cloudinary.uploader

cloudinary.config(
    cloud_name="ddacq5ltb",
    api_key="985616939343421",
    api_secret="oI07cgZ3rGa0VJ8DW354oQV013g"
)

class ReviewService:
    def get_all_review(self, session: Session):
        statement = select(Reviews).order_by(desc(Reviews.created_at))
        result = session.execute(statement)
        reviews = result.scalars().all()
        for review in reviews:
            self.add_image_host(review)
        return reviews

    def get_singleReview(self, review_uid: uuid.UUID, session: Session):
        statement = select(Reviews).where(Reviews.uid == review_uid.bytes)
        result = session.execute(statement)
        review = result.scalar_one_or_none()
        if review:
            self.add_image_host(review)
        return review

    def save_image(self, image_file: UploadFile) -> Optional[str]:
        """Save single image to Cloudinary and return URL"""
        if not image_file:
            return None

        try:
            result = cloudinary.uploader.upload(
                image_file.file,
                folder="blog_images",
                public_id=f"img_{uuid.uuid4().hex}",
                resource_type="auto"
            )
            return result['secure_url']
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None

    def create_review(self, review_data: CreateReview, image_file: Optional[UploadFile], session: Session):
        image_path = self.save_image(image_file) if image_file else None

        new_review = Reviews(
            name=review_data.name,
            review=review_data.review,
            position=review_data.position,
            image=image_path
        )

        session.add(new_review)
        session.commit()
        session.refresh(new_review)

        self.add_image_host(new_review)
        return new_review

    def update_review(self, review_uid: uuid.UUID, review_update_data: UpdateReview, image_file: Optional[UploadFile], session: Session):
        review = session.query(Reviews).filter(Reviews.uid == review_uid.bytes).first()
        if not review:
            return None

        # Delete old image if new one is provided
        if image_file and review.image and os.path.exists(review.image):
            os.remove(review.image)

        # Only update fields that were actually provided
        update_data = review_update_data.dict(exclude_unset=True)
        for attr, value in update_data.items():
            setattr(review, attr, value)

        if image_file:
            review.image = self.save_image(image_file)

        review.updated_at = datetime.now()
        session.commit()
        session.refresh(review)
        
        self.add_image_host(review)
        return review
    
    def delete_review(self, review_uid: uuid.UUID, session: Session):
        review = session.query(Reviews).filter(Reviews.uid == review_uid.bytes).first()
        if review:
            if review.image and os.path.exists(review.image):
                os.remove(review.image)

            session.delete(review)
            session.commit()
            return True
        return False

    def add_image_host(self, review: Reviews):
        if review and review.image and not review.image.startswith("http"):
            review.image = f"{BASE_URL}{review.image}"