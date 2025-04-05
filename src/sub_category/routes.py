from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from src.db.database import get_session
from src.sub_category.service import SubCategoriesService
from src.sub_category.schemas import SubCategory, CreateSubCategory, UpdateSubCategory


sub_category_router = APIRouter()
sub_category_service = SubCategoriesService()


@sub_category_router.get("/", response_model=List[SubCategory])
def get_all_subcategories(session: Session = Depends(get_session)):
    sub_categories = sub_category_service.get_all_subcategories(session)
    return sub_categories


@sub_category_router.post("/", response_model=SubCategory, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    name: str = Form(...),
    image_file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):
    subcategory_data = CreateSubCategory(name=name)
    new_subcategory = sub_category_service.create_subcategory(subcategory_data, image_file, session)
    return new_subcategory


@sub_category_router.get("/{sub_category_uid}", response_model=SubCategory)
def get_subcategory(sub_category_uid: uuid.UUID, session: Session = Depends(get_session)):
    sub_category = sub_category_service.get_subcategory(sub_category_uid, session)
    if sub_category:
        return sub_category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sub-category not found")


@sub_category_router.get("/image/{sub_category_uid}")
def get_subcategory_image(sub_category_uid: uuid.UUID, session: Session = Depends(get_session)):
    sub_category = sub_category_service.get_subcategory(sub_category_uid, session)
    if sub_category and sub_category.image and os.path.exists(sub_category.image):
        return FileResponse(sub_category.image, media_type={
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


@sub_category_router.patch("/{sub_category_uid}", response_model=SubCategory)
def update_subcategory(
    sub_category_uid: uuid.UUID,
    name: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):
     # Get the subcategory by UID
    sub_category_update_data = UpdateSubCategory(name=name)  # Only pass name if provided

    updated_sub_category = sub_category_service.update_subcategory(
        sub_category_uid, sub_category_update_data, image_file, session
    )
    if updated_sub_category:
        return updated_sub_category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sub-category not found")

@sub_category_router.delete("/{sub_category_uid}")
def delete_subcategory(sub_category_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = sub_category_service.delete_subcategory(sub_category_uid, session)
    if deleted:
        return {"message": "subCategory deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="subCategory not found")
