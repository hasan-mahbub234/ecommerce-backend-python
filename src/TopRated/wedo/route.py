from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from .service import WedoService
from .schema import CreateWedo, UpdateWedo, Wedo
from typing import List, Optional
import uuid
from fastapi.responses import FileResponse
import os

wedo_router = APIRouter()
wedo_service = WedoService()

@wedo_router.get("/", response_model=List[Wedo])
def all_wedos(session: Session = Depends(get_session)):
    wedos = wedo_service.get_all_wedo(session)
    return wedos

@wedo_router.post("/", response_model=Wedo, status_code=status.HTTP_201_CREATED)
def create_expert(
    title: str = Form(...),
    desc: str = Form(...),
    service: str = Form(...),
    image_file: UploadFile = File(),
    session: Session = Depends(get_session)
):
    service_list = [s.strip() for s in service.split(",")] if service else []
    
    wedo_data = CreateWedo(
        title=title, desc=desc, service=service_list
    )
    new_wedo = wedo_service.create_wedo(wedo_data, image_file, session)

    return new_wedo


@wedo_router.get("/{wedo_uid}", response_model=Wedo)
def single_wedo(wedo_uid: uuid.UUID, session: Session = Depends(get_session)):
    wedo = wedo_service.get_singleWedo(wedo_uid, session)
    if wedo:
        return wedo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Wedo not found"
    )

@wedo_router.patch("/{wedo_uid}", response_model=Wedo)
def update_wedo(
    wedo_uid: uuid.UUID,
    title: Optional[str] = Form(None),
    desc: Optional[str] = Form(None),
    service: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):
    # Parse technology string to list if provided
    service_list = None
    if service is not None:
        service_list = [s.strip() for s in service.split(",")] if service else []
    
    # Create update data with only provided fields
    update_data = {}
    if title is not None:
        update_data['title'] = title
    if desc is not None:
        update_data['desc'] = desc
    if service_list is not None:
        update_data['service'] = service_list
    
    wedo_update_data = UpdateWedo(**update_data)
    
    updated_wedo = wedo_service.update_wedo(
        wedo_uid, wedo_update_data, image_file, session
    )
    if updated_wedo:
        return updated_wedo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Wedo not found"
    )

@wedo_router.delete("/{wedo_uid}",)
def delete_wedo(wedo_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = wedo_service.delete_wedo(wedo_uid, session)
    if deleted:
        return {"message": "Wedo deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wedo not found")
