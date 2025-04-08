from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .model import Experts
from .schema import ExpertCreate, ExpertUpdate
import uuid
from datetime import datetime
from fastapi import UploadFile
import os
from typing import Optional
from ..blogs.service import BASE_URL

UPLOAD_FOLDER = "uploads/"

class ExpertService:
    def get_all_expert(self, session: Session):
        statement = select(Experts).order_by(desc(Experts.created_at))
        result = session.execute(statement)
        experts = result.scalars().all()
        for expert in experts:
            self.add_image_host(expert)
        return experts

    def get_singleExpert(self, expert_uid: uuid.UUID, session: Session):
        statement = select(Experts).where(Experts.uid == expert_uid.bytes)
        result = session.execute(statement)
        expert = result.scalar_one_or_none()
        if expert:
            self.add_image_host(expert)
        return expert

    def save_image(self, image_file: UploadFile) -> Optional[str]:
        """Save image to disk and return the file path"""
        if not image_file:
            return None

        file_extension = image_file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        with open(file_path, "wb") as buffer:
            buffer.write(image_file.file.read())

        return file_path

    def create_expert(self, expert_data: ExpertCreate, image_file: Optional[UploadFile], session: Session):
        image_path = self.save_image(image_file) if image_file else None

        new_expert = Experts(
            name=expert_data.name,
            exp=expert_data.exp,
            type=expert_data.type,
            technology=expert_data.technology,
            image=image_path
        )

        session.add(new_expert)
        session.commit()
        session.refresh(new_expert)

        self.add_image_host(new_expert)
        return new_expert

    def update_expert(self, expert_uid: uuid.UUID, expert_update_data: ExpertUpdate, image_file: Optional[UploadFile], session: Session):
        expert = session.query(Experts).filter(Experts.uid == expert_uid.bytes).first()
        if not expert:
            return None

        # Delete old image if new one is provided
        if image_file and expert.image and os.path.exists(expert.image):
            os.remove(expert.image)

        # Only update fields that were actually provided
        update_data = expert_update_data.dict(exclude_unset=True)
        for attr, value in update_data.items():
            setattr(expert, attr, value)

        if image_file:
            expert.image = self.save_image(image_file)

        expert.updated_at = datetime.now()
        session.commit()
        session.refresh(expert)
        
        self.add_image_host(expert)
        return expert
    
    def delete_expert(self, expert_uid: uuid.UUID, session: Session):
        expert = session.query(Experts).filter(Experts.uid == expert_uid.bytes).first()
        if expert:
            if expert.image and os.path.exists(expert.image):
                os.remove(expert.image)

            session.delete(expert)
            session.commit()
            return True
        return False

    def add_image_host(self, expert: Experts):
        if expert and expert.image and not expert.image.startswith("http"):
            expert.image = f"{BASE_URL}{expert.image}"
