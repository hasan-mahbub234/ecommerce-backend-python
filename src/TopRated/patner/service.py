from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .model import Patners
from .schema import PatnerCreate, PatnerUpdate
import uuid
from datetime import datetime
from fastapi import UploadFile
import os
from typing import Optional
from ..blogs.service import BASE_URL

UPLOAD_FOLDER = "uploads/"

class PatnerService:
    def add_logo_host(self, patner: Patners):
        if patner and patner.logo and not patner.logo.startswith("http"):
            patner.logo = f"{BASE_URL}{patner.logo}"

    def get_all_patners(self, session: Session):
        statement = select(Patners).order_by(desc(Patners.created_at))
        result = session.execute(statement)
        patners = result.scalars().all()
        for patner in patners:
            self.add_logo_host(patner)
        return patners
    
    def get_singlePatner(self, patner_uid: uuid.UUID, session: Session):
        statement = select(Patners).where(Patners.uid == patner_uid.bytes)
        result = session.execute(statement)
        patner = result.scalar_one_or_none()
        if patner:
            self.add_logo_host(patner)
        return patner
    
    def save_logo(self, logo_file: UploadFile) -> Optional[str]:
        """Save logo to disk and return the file path"""
        if not logo_file:
            return None

        file_extension = logo_file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        with open(file_path, "wb") as buffer:
            buffer.write(logo_file.file.read())

        return file_path
    
    def create_patner(self, patner_data: PatnerCreate, logo_file: Optional[UploadFile], session: Session):
        logo_path = self.save_logo(logo_file) if logo_file else None

        new_patner = Patners(
            name=patner_data.name,
            logo=logo_path
        )

        session.add(new_patner)
        session.commit()
        session.refresh(new_patner)

        self.add_logo_host(new_patner)
        return new_patner
    
    def update_patner(self, patner_uid: uuid.UUID, patner_update_data: PatnerUpdate, logo_file: Optional[UploadFile], session: Session):
        patner = session.query(Patners).filter(Patners.uid == patner_uid.bytes).first()
        if not patner:
            return None

        # Delete old logo if new one is provided
        if logo_file and patner.logo and os.path.exists(patner.logo):
            os.remove(patner.logo)

        # for attr in ['name']:
        #     setattr(patner, attr, getattr(patner_update_data, attr, getattr(patner, attr)))

        if patner.name:
            patner.name = patner_update_data.name

        if logo_file:
            patner.logo = self.save_logo(logo_file)

        patner.updated_at = datetime.now()
        session.commit()
        session.refresh(patner)
        
        self.add_logo_host(patner)
        return patner
    
    def delete_patner(self, patner_uid: uuid.UUID, session: Session):
        patner = session.query(Patners).filter(Patners.uid == patner_uid.bytes).first()
        if patner:
            if patner.logo and os.path.exists(patner.logo):
                os.remove(patner.logo)

            session.delete(patner)
            session.commit()
            return True
        return False