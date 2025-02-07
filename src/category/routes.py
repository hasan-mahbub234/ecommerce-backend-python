from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_session
from src.category.services import CategoriesService
from src.category.schemas import Categories, CreateCategories, UpdateCategories
from typing import List
import uuid

category_router = APIRouter()
category_service = CategoriesService()  # Initialize the service correctly

@category_router.get("/", response_model=List[Categories])
def all_categories(session: Session = Depends(get_session)):
    categories = category_service.get_all_categories(session)
    return categories

@category_router.post("/",response_model=Categories, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CreateCategories, session: Session = Depends(get_session)):
    new_category = category_service.create_category(category_data, session)
    return new_category

@category_router.get("/{category_uid}", response_model=Categories)
def single_category(category_uid: uuid.UUID, session: Session = Depends(get_session)):
    category = category_service.get_category(category_uid, session)
    if category:
        return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

@category_router.patch("/{category_uid}", response_model=Categories)
def update_category(category_uid: uuid.UUID, category_update_data: UpdateCategories, session: Session = Depends(get_session)):
    updated_category = category_service.update_category(category_uid, category_update_data, session)
    if updated_category:
        return updated_category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

@category_router.delete("/{category_uid}",)
def delete_category(category_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = category_service.delete_category(category_uid, session)
    if deleted:
        return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
