from fastapi import APIRouter, Depends, HTTPException, status,  UploadFile, File, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from src.products.service import ProductService
from src.products.schemas import Products, CreateProduct, UpdateProduct
from typing import List, Optional
import uuid
from fastapi.responses import FileResponse
import os

product_router = APIRouter()
product_service = ProductService()  # Initialize the service correctly

@product_router.get("/", response_model=List[Products])
def all_products(session: Session = Depends(get_session)):
    products = product_service.get_all_products(session)
    return products

@product_router.post("/",response_model= Products, status_code=status.HTTP_201_CREATED)
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
    product_data = CreateProduct(name=name,  quantity =quantity, description= description, price=price, brand=brand, category=category, sub_category=sub_category,age=age, discount=discount)
    new_product = product_service.create_product(product_data, image_file, video_file, session)
    return new_product

@product_router.get("/{product_uid}", response_model= Products)
def single_product(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    product = product_service.get_product(product_uid, session)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail="Product not found")

@product_router.get("/image/{category_uid}")
def get_product_image(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    product = product_service.get_product(product_uid, session)
    if product and product.image and os.path.exists(product.image):
        return FileResponse(product.image, media_type={
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

@product_router.get("/video/{product_uid}")
def get_product_video(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    product = product_service.get_product(product_uid, session)
    if product and product.video and os.path.exists(product.video):
        return FileResponse(product.video, media_type={
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo",
            ".wmv": "video/x-ms-wmv",
            ".flv": "video/x-flv",
            ".webm": "video/webm",
            ".mkv": "video/x-matroska",
            ".3gp": "video/3gpp",
            ".mpeg": "video/mpeg",
            ".ogg": "video/ogg"
        })  # Adjust MIME type as needed
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

@product_router.patch("/{product_uid}", response_model= Products)
def update_product(product_uid: uuid.UUID, 
    name: str = Form(None),
    quantity: int = Form(None),
    description: str = Form(None),
    price: int = Form(None),
    brand: str = Form(None),
    category: str = Form(None),
    image_file: Optional[UploadFile] = File(None),
    video_file: Optional[UploadFile] = File(None),
    sub_category: Optional[str] = Form(None),
    age: Optional[str] = Form(None),
    discount: Optional[int] = Form(None),
    session: Session = Depends(get_session)):

    product_update_data = UpdateProduct(name=name, quantity=quantity, description= description, price=price, brand=brand, category=category, sub_category=sub_category, age=age, discount=discount)

    updated_product = product_service.update_product(
        product_uid, product_update_data, image_file, video_file, session
    )
    if updated_product:
        return updated_product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    

@product_router.delete("/{product_uid}",)
def delete_product(product_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = product_service.delete_product(product_uid, session)
    if deleted:
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
