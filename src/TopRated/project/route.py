from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from .service import ProjectService
from .schema import ProjectCreate, ProjectUpdate, Project
from typing import List, Optional
import uuid
from pydantic import ValidationError
import json

project_router = APIRouter(tags=["Projects"])
project_service = ProjectService()

@project_router.get("/", response_model=List[Project])
def list_projects(session: Session = Depends(get_session)):
    return project_service.get_all_projects(session)

@project_router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    name: str = Form(...),
    desc: str = Form(...),
    email: str = Form(...),
    type: str = Form(...), 
    session: Session = Depends(get_session)
):
    type_list = [t.strip() for t in type.split(",")] if type else []

    project_data = ProjectCreate(
        name=name, desc=desc, email=email, type=type_list
    )
    new_project = project_service.create_project(project_data, session)

    return new_project

@project_router.get("/{project_uid}", response_model=Project)
def get_project(project_uid: uuid.UUID, session: Session = Depends(get_session)):
    project = project_service.get_single_project(project_uid, session)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@project_router.patch("/{project_uid}", response_model=Project)
def update_project(
    project_uid: uuid.UUID,
    name: Optional[str] = Form(None),
    desc: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    if type is not None:
        type_list = [t.strip() for t in type.split(",")] if type else []

    update_data = {}
    if name is not None:
        update_data['name'] = name
    if desc is not None:
        update_data['desc'] = desc
    if email is not None:
        update_data['email'] = email
    if type_list is not None:
        update_data['type'] = type_list

    project_update_data = ProjectUpdate(**update_data)
    updated_project = project_service.update_project(project_uid, project_update_data, session)

    if updated_project:
        return updated_project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found"
    )
    

@project_router.delete("/{project_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_uid: uuid.UUID, session: Session = Depends(get_session)):
    if not project_service.delete_project(project_uid, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )