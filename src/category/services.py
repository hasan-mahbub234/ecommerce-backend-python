from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .models import Categories
from .schemas import CreateCategories, UpdateCategories
import uuid
from datetime import datetime
import os
from typing import Optional
from fastapi import UploadFile

UPLOAD_FOLDER = "uploads/"  # Folder to store images

class CategoriesService:
    def get_all_categories(self, session: Session):
        statement = select(Categories).order_by(desc(Categories.created_at))
        result = session.execute(statement)
        return result.scalars().all()

    def get_category(self, category_uid: uuid.UUID, session: Session):
        statement = select(Categories).where(Categories.uid == category_uid.bytes)
        result = session.execute(statement)
        category = result.scalar_one_or_none()

        if category and category.image:
            category.image = f"http://localhost:8000/{category.image}"
        return category
    
    def save_image(self, image_file: UploadFile) -> str:
        """ Save image to disk and return the file path """
        if not image_file:
            return None

        file_extension = image_file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure directory exists

        with open(file_path, "wb") as buffer:
            buffer.write(image_file.file.read())

        return file_path  # Return the relative file path

    def create_category(self, category_data: CreateCategories, image_file: Optional[UploadFile], session: Session):
        image_path = self.save_image(image_file) if image_file else None

        new_category = Categories(
            name=category_data.name,
            sub_category= category_data.sub_category,
            image=image_path
        )

        session.add(new_category)
        session.commit()
        session.refresh(new_category)

        # Return the full URL to the image after creating the category
        if new_category.image:
            new_category.image = f"http://localhost:8000/{new_category.image}"

        return new_category

    def update_category(self, category_uid: uuid.UUID, category_update_data: UpdateCategories, image_file: Optional[UploadFile], session: Session):
        category = session.query(Categories).filter(Categories.uid == category_uid.bytes).first()

        if not category:
            return None

        if image_file and category.image and os.path.exists(category.image):
            os.remove(category.image)

        if category_update_data.name:
            category.name = category_update_data.name

        if category_update_data.sub_category:
            category.sub_category = category_update_data.sub_category

        if image_file:
            category.image = self.save_image(image_file)


        category.updated_at = datetime.now()

        session.commit()
        session.refresh(category)

        # Return the full URL to the image after updating the category
        if category.image:
            category.image = f"http://localhost:8000/{category.image}"

        return category
    
    def delete_category(self, category_uid: uuid.UUID, session: Session):
        category = session.query(Categories).filter(Categories.uid == category_uid.bytes).first()
        if category:
            if category.image and os.path.exists(category.image):
                os.remove(category.image)
            session.delete(category)
            session.commit()
            return True
        return False


