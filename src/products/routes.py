from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from src.products.service import ProductService
from src.products.schemas import Products, CreateProduct, UpdateProduct
from typing import List, Optional
import uuid
from fastapi.responses import FileResponse
import os

product_router = APIRouter(prefix="/api/v1/product", tags=["products"])
product_service = ProductService()

@product_router.get("/", response_model=List[Products])
def all_products(session: Session = Depends(get_session)):
    return product_service.get_all_products(session)

@product_router.post("/", response_model=Products, status_code=status.HTTP_201_CREATED)
def create_product(
    name: str = Form(...),
    quantity: int = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    brand: str = Form(...),
    category: str = Form(...),
    image_file: Optional[UploadFile] = File(None),
    video_file: Optional[UploadFile] = File(None),
    sub_category: Optional[str] = Form(None),
    age: Optional[str] = Form(None),
    discount: Optional[int] = Form(None),
    session: Session = Depends(get_session)
):
    product_data = CreateProduct(
        name=name,
        quantity=quantity,
        description=description,
        price=price,
        brand=brand,
        category=category,
        sub_category=sub_category,
        age=age,
        discount=discount
    )
    return product_service.create_product(product_data, image_file, video_file, session)

@product_router.get("/{product_uid}", response_model=Products)
def single_product(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    product = product_service.get_product(product_uid, session)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@product_router.get("/image/{product_uid}")
def get_product_image(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    product = product_service.get_product(product_uid, session)
    if not product or not product.image or not os.path.exists(product.image):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    return FileResponse(product.image)

@product_router.get("/video/{product_uid}")
def get_product_video(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    product = product_service.get_product(product_uid, session)
    if not product or not product.video or not os.path.exists(product.video):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    
    return FileResponse(product.video)

@product_router.patch("/{product_uid}", response_model=Products)
def update_product(
    product_uid: uuid.UUID,
    name: Optional[str] = Form(None),
    quantity: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[int] = Form(None),
    brand: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None),
    video_file: Optional[UploadFile] = File(None),
    sub_category: Optional[str] = Form(None),
    age: Optional[str] = Form(None),
    discount: Optional[int] = Form(None),
    session: Session = Depends(get_session)
):
    product_update_data = UpdateProduct(
        name=name,
        quantity=quantity,
        description=description,
        price=price,
        brand=brand,
        category=category,
        sub_category=sub_category,
        age=age,
        discount=discount
    )
    
    updated_product = product_service.update_product(
        product_uid, product_update_data, image_file, video_file, session
    )
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated_product

@product_router.delete("/{product_uid}")
def delete_product(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    if not product_service.delete_product(product_uid, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully"}