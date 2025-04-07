from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from .service import ExpertService
from .schema import ExpertCreate, ExpertUpdate, Expert
from typing import List, Optional
import uuid
from fastapi.responses import FileResponse
import os

expert_router = APIRouter()
expert_service = ExpertService()

@expert_router.get("/", response_model=List[Expert])
def all_experts(session: Session = Depends(get_session)):
    experts = expert_service.get_all_expert(session)
    return experts

@expert_router.post("/", response_model=Expert, status_code=status.HTTP_201_CREATED)
def create_expert(
    name: str = Form(...),
    type: str = Form(...),
    exp: str = Form(...),
    technology: List[str] = Form(...),
    image_file: UploadFile = File(),
    session: Session = Depends(get_session)
):
    expert_data = ExpertCreate(
        name=name, type=type, exp=exp, technology=technology
    )
    new_expert = expert_service.create_expert(expert_data, image_file, session)

    return new_expert

@expert_router.get("/image/{expert_uid}")
def get_product_image(expert_uid: uuid.UUID, session: Session = Depends(get_session)):
    expert = expert_service.get_singleExpert(expert_uid, session)
    if expert and expert.image and os.path.exists(expert.image):
        return FileResponse(expert.image, media_type={
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".tiff": "image/tiff",
            ".ico": "image/vnd.microsoft.icon",
            ".svg": "image/svg+xml"
        })  # Adjust MIME type as needed
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

@expert_router.get("/{expert_uid}", response_model=Expert)
def single_expert(expert_uid: uuid.UUID, session: Session = Depends(get_session)):
    expert = expert_service.get_singleExpert(expert_uid, session)
    if expert:
        return expert
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expert not found"
    )

@expert_router.patch("/{expert_uid}", response_model=Expert)
def update_expert(
    expert_uid: uuid.UUID,
    name: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    exp: Optional[str] = Form(None),
    technology: Optional[str] = Form(None),  # Receive as string
    image_file: Optional[UploadFile] = File(None),  # Make optional
    session: Session = Depends(get_session)
):
    # Parse technology string to list if provided
    technology_list = None
    if technology is not None:
        technology_list = [tech.strip() for tech in technology.split(",")] if technology else []
    
    expert_update_data = ExpertUpdate(
        name=name,
        type=type,
        exp=exp,
        technology=technology_list  # Pass the parsed list
    )
    
    updated_expert = expert_service.update_expert(
        expert_uid, expert_update_data, image_file, session
    )
    if updated_expert:
        return updated_expert
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expert not found"
    )

@expert_router.delete("/{expert_uid}",)
def delete_expert(expert_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = expert_service.delete_expert(expert_uid, session)
    if deleted:
        return {"message": "Expert deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expert not found")
