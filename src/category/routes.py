from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
from sqlalchemy.orm import Session
from src.db.database import get_session
from src.category.services import CategoriesService
from src.category.schemas import Categories, CreateCategories, UpdateCategories, SubCategory
from typing import List
import uuid
from typing import List, Optional


category_router = APIRouter()
category_service = CategoriesService()


@category_router.get("/", response_model=List[Categories])
def all_categories(session: Session = Depends(get_session)):
    categories = category_service.get_all_categories(session)
    return categories


@category_router.post("/", response_model=Categories, status_code=status.HTTP_201_CREATED)
def create_category(
    name: str = Form(...),
    sub_category: Optional[List[SubCategory]] = Form(None),
    image_file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):
    category_data = CreateCategories(name=name, sub_category=sub_category)
    new_category = category_service.create_category(category_data, image_file, session)
    return new_category


@category_router.get("/{category_uid}", response_model=Categories)
def single_category(category_uid: uuid.UUID, session: Session = Depends(get_session)):
    category = category_service.get_category(category_uid, session)
    if category:
        return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

@category_router.get("/image/{category_uid}")
def get_category_image(category_uid: uuid.UUID, session: Session = Depends(get_session)):
    category = category_service.get_category(category_uid, session)
    if category and category.image and os.path.exists(category.image):
        return FileResponse(category.image, media_type={
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

@category_router.patch("/{category_uid}", response_model=Categories)
def update_category(
    category_uid: uuid.UUID,
    name: Optional[str] = Form(None),
    sub_category: Optional[List[SubCategory]] = Form(None),
    image_file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):
    category_update_data = UpdateCategories(name=name, sub_category=sub_category)

    updated_category = category_service.update_category(
        category_uid, category_update_data, image_file, session
    )
    if updated_category:
        return updated_category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@category_router.delete("/{category_uid}")
def delete_category(category_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = category_service.delete_category(category_uid, session)
    if deleted:
        return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")