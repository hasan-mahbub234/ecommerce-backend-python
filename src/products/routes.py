from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_session
from src.products.service import ProductService
from src.products.schemas import Products, CreateProduct, UpdateProduct
from typing import List
import uuid

product_router = APIRouter()
product_service = ProductService()  # Initialize the service correctly

@product_router.get("/", response_model=List[Products])
def all_products(session: Session = Depends(get_session)):
    products = product_service.get_all_products(session)
    return products

@product_router.post("/",response_model= Products, status_code=status.HTTP_201_CREATED)
def create_product(product_data: CreateProduct, session: Session = Depends(get_session)):
    new_product = product_service.create_product(product_data, session)
    return new_product

@product_router.get("/{product_uid}", response_model= Products)
def single_product(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    product = product_service.get_product(product_uid, session)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@product_router.patch("/{product_uid}", response_model= Products)
def update_product(product_uid: uuid.UUID, product_update_data: UpdateProduct, session: Session = Depends(get_session)):
    updated_product = product_service.update_product(product_uid, product_update_data, session)
    if updated_product:
        return updated_product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@product_router.delete("/{product_uid}",)
def delete_product(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = product_service.delete_product(product_uid, session)
    if deleted:
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
