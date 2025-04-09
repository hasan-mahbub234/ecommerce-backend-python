from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .model import Wedos
from .schema import CreateWedo, UpdateWedo
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

class WedoService:
    def get_all_wedo(self, session: Session):
        statement = select(Wedos).order_by(desc(Wedos.created_at))
        result = session.execute(statement)
        wedos = result.scalars().all()
        for wedo in wedos:
            self.add_image_host(wedo)
        return wedos

    def get_singleWedo(self, wedo_uid: uuid.UUID, session: Session):
        statement = select(Wedos).where(Wedos.uid == wedo_uid.bytes)
        result = session.execute(statement)
        wedo = result.scalar_one_or_none()
        if wedo:
            self.add_image_host(wedo)
        return wedo

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

    def create_wedo(self, wedo_data: CreateWedo, image_file: Optional[UploadFile], session: Session):
        image_path = self.save_image(image_file) if image_file else None

        new_wedo = Wedos(
            title=wedo_data.title,
            desc=wedo_data.desc,
            service=wedo_data.service,
            image=image_path
        )

        session.add(new_wedo)
        session.commit()
        session.refresh(new_wedo)

        self.add_image_host(new_wedo)
        return new_wedo

    def update_wedo(self, wedo_uid: uuid.UUID, wedo_update_data: UpdateWedo, image_file: Optional[UploadFile], session: Session):
        wedo = session.query(Wedos).filter(Wedos.uid == wedo_uid.bytes).first()
        if not wedo:
            return None

        # Delete old image if new one is provided
        if image_file and wedo.image and os.path.exists(wedo.image):
            os.remove(wedo.image)

        # Only update fields that were actually provided
        update_data = wedo_update_data.dict(exclude_unset=True)
        for attr, value in update_data.items():
            setattr(wedo, attr, value)

        if image_file:
            wedo.image = self.save_image(image_file)

        wedo.updated_at = datetime.now()
        session.commit()
        session.refresh(wedo)
        
        self.add_image_host(wedo)
        return wedo
    
    def delete_wedo(self, wedo_uid: uuid.UUID, session: Session):
        wedo = session.query(Wedos).filter(Wedos.uid == wedo_uid.bytes).first()
        if wedo:
            if wedo.image and os.path.exists(wedo.image):
                os.remove(wedo.image)

            session.delete(wedo)
            session.commit()
            return True
        return False

    def add_image_host(self, wedo: Wedos):
        if wedo and wedo.image and not wedo.image.startswith("http"):
            wedo.image = f"{BASE_URL}{wedo.image}"
