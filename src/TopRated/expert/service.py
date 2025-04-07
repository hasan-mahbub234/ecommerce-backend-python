from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .model import Experts
from .schema import ExpertCreate, ExpertUpdate
import uuid
from datetime import datetime
from fastapi import UploadFile
import os
from typing import Optional

UPLOAD_FOLDER = "uploads/"

class ExpertService:
    def get_all_expert(self, session: Session):
        statement = select(Experts).order_by(desc(Experts.created_at))
        result = session.execute(statement)
        return result.scalars().all()

    def get_singleExpert(self, expert_uid: uuid.UUID, session: Session):
        statement = select(Experts).where(Experts.uid == expert_uid.bytes)
        result = session.execute(statement)
        expert = result.scalar_one_or_none()

        if expert and expert.image:
            expert.image = f"https://api.toprateddesigner.com/{expert.image}"
        return expert
    

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

        return file_path
    
    def create_expert(self, expert_data: ExpertCreate, image_file: Optional[UploadFile],session: Session):
        image_path = self.save_image(image_file) if image_file else None
    
        new_expert = Experts(
            name= expert_data.name,
            exp = expert_data.exp,
            type = expert_data.type,
            techology= expert_data.technology,
            image=image_path
        )

        session.add(new_expert)
        session.commit()
        session.refresh(new_expert)

        # Return the full URL to the image after creating the product
        if new_expert.image:
            new_expert.image = f"https://api.toprateddesigner.com/{new_expert.image}"

        return new_expert
    
    def update_expert(self, expert_uid: uuid.UUID, expert_update_data: ExpertUpdate, image_file: UploadFile, session: Session):
        
        expert = session.query(Experts).filter(Experts.uid == expert_uid.bytes).first()

        if not expert:
            return None
        if image_file and expert.image and os.path.exists(expert.image):
            os.remove(expert.image)
        for attr in ['name', 'type', 'exp', 'technology'] :
            setattr(expert, attr, getattr(expert_update_data, attr, getattr(expert, attr)))

        if image_file:
            expert.image = self.save_image(image_file)

        expert.updated_at = datetime.now()
        session.commit()
        session.refresh(expert)
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

