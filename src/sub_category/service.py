from fastapi import UploadFile
import os
from typing import Optional
from sqlmodel import desc, select
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from src.sub_category.models import SubCategories
from src.sub_category.schemas import CreateSubCategory, UpdateSubCategory

UPLOAD_FOLDER = "uploads/"  # Folder to store images

class SubCategoriesService:
    def get_all_subcategories(self, session: Session):
        statement = select(SubCategories).order_by(desc(SubCategories.created_at))
        result = session.execute(statement)
        return result.scalars().all()

    def get_subcategory(self, subcategory_uid: uuid.UUID, session: Session):
        statement = select(SubCategories).where(SubCategories.uid == subcategory_uid.bytes)
        result = session.execute(statement)
        subcategory = result.scalar_one_or_none()
        if subcategory and subcategory.image:
            # Return the full URL to the image
            subcategory.image = f"http://localhost:8000/{subcategory.image}"
        return subcategory

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

    def create_subcategory(self, subcategory_data: CreateSubCategory, image_file: Optional[UploadFile], session: Session):
        image_path = self.save_image(image_file) if image_file else None

        new_subcategory = SubCategories(
            name=subcategory_data.name,
            image=image_path
        )

        session.add(new_subcategory)
        session.commit()
        session.refresh(new_subcategory)

        # Return the full URL to the image after creating the subcategory
        if new_subcategory.image:
            new_subcategory.image = f"http://localhost:8000/{new_subcategory.image}"

        return new_subcategory

    def update_subcategory(self, subcategory_uid: uuid.UUID, subcategory_update_data: UpdateSubCategory, image_file: Optional[UploadFile], session: Session):
        subcategory = session.query(SubCategories).filter(SubCategories.uid == subcategory_uid.bytes).first()

        if not subcategory:
            return None

        if image_file and subcategory.image and os.path.exists(subcategory.image):
            os.remove(subcategory.image)  # Remove the old image file from the uploads folder

         # Update fields if provided in the subcategory_update_data
        if subcategory_update_data.name:  # Check if name is provided
            subcategory.name = subcategory_update_data.name

        # Handle image separately
        if image_file:
            subcategory.image = self.save_image(image_file)

        subcategory.updated_at = datetime.now()

        session.commit()
        session.refresh(subcategory)

        # Return full URL for image
        if subcategory.image:
            subcategory.image = f"http://localhost:8000/{subcategory.image}"

        return subcategory


    def delete_subcategory(self, subcategory_uid: uuid.UUID, session: Session):
        subcategory = session.query(SubCategories).filter(SubCategories.uid == subcategory_uid.bytes).first()
        if subcategory:
                        # Delete the image file if it exists
            if subcategory.image and os.path.exists(subcategory.image):
                os.remove(subcategory.image)  # Remove the image file from the uploads folder
            session.delete(subcategory)
            session.commit()
            return True
        return False
