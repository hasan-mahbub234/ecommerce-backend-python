from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from .service import PatnerService
from .schema import PatnerCreate, PatnerUpdate, Patners
from typing import List, Optional
import uuid
from fastapi.responses import FileResponse
import os

patner_router = APIRouter()
patner_service = PatnerService()

@patner_router.get("/", response_model=List[Patners])
def all_patners(session: Session = Depends(get_session)):
    patners = patner_service.get_all_patners(session)
    return patners

@patner_router.post("/", response_model=Patners, status_code=status.HTTP_201_CREATED)
def create_patner(
    name: str = Form(...),
    logo_file: UploadFile = File(),
    session: Session = Depends(get_session)
):
    patner_data = PatnerCreate(
        name=name
    )
    new_patner = patner_service.create_patner(patner_data, logo_file, session)

    return new_patner


@patner_router.get("/{patner_uid}", response_model=Patners)
def single_patner(patner_uid: uuid.UUID, session: Session = Depends(get_session)):
    patner = patner_service.get_singlePatner(patner_uid, session)
    if patner:
        return patner
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Patner not found"
    )

@patner_router.patch("/{patner_uid}", response_model=Patners)
def update_patner(
    patner_uid: uuid.UUID,
    name: Optional[str] = Form(None),
    logo_file: Optional[UploadFile] = File(None),  # Make optional
    session: Session = Depends(get_session)
):

    
    patner_update_data = PatnerUpdate(
        name=name,
    )
    
    updated_patner = patner_service.update_patner(
        patner_uid, patner_update_data, logo_file, session
    )
    if updated_patner:
        return updated_patner
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Patner not found"
    )

@patner_router.delete("/{patner_uid}",)
def delete_patner(patner_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = patner_service.delete_patner(patner_uid, session)
    if deleted:
        return {"message": "Patner deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patner not found")