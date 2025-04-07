from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .models import Products
from .schemas import CreateProduct, UpdateProduct
import uuid
from datetime import datetime
from fastapi import UploadFile
import os
from typing import Optional

UPLOAD_FOLDER = "uploads/"

class ProductService:
    def get_all_products(self, session: Session):
        statement = select(Products).order_by(desc(Products.created_at))
        result = session.execute(statement)
        return result.scalars().all()

    def get_product(self, product_uid: uuid.UUID, session: Session):
        statement = select(Products).where(Products.uid == product_uid.bytes)
        result = session.execute(statement)
        product = result.scalar_one_or_none()

        if product and product.image:
            product.image = f"https://api.toprateddesigner.com/{product.image}"
        if product and product.video:
            product.video = f"https://api.toprateddesigner.com/{product.video}"
        return product
    
    def save_file(self, file: UploadFile, subfolder: str = "") -> str:
        """Save file to disk and return the file path"""
        if not file:
            return None

        file_extension = file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, subfolder, file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        return file_path

    def create_product(self, product_data: CreateProduct, image_file: Optional[UploadFile], video_file: Optional[UploadFile], session: Session):
        image_path = self.save_file(image_file, "images") if image_file else None
        video_path = self.save_file(video_file, "videos") if video_file else None

        new_product = Products(
            name=product_data.name,
            quantity=product_data.quantity,
            brand=product_data.brand,
            price=product_data.price,
            description=product_data.description,
            category=product_data.category,
            sub_category=product_data.sub_category,
            age=product_data.age,
            discount=product_data.discount,
            video=video_path,
            image=image_path
        )

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        if new_product.image:
            new_product.image = f"https://api.toprateddesigner.com/{new_product.image}"
        if new_product.video:
            new_product.video = f"https://api.toprateddesigner.com/{new_product.video}"

        return new_product

    def update_product(self, product_uid: uuid.UUID, product_update_data: UpdateProduct, image_file: Optional[UploadFile], video_file: Optional[UploadFile], session: Session):
        product = session.query(Products).filter(Products.uid == product_uid.bytes).first()
        if not product:
            return None
        
        # Delete old files if they exist and new files are being uploaded
        if image_file and product.image and os.path.exists(product.image):
            os.remove(product.image)
        if video_file and product.video and os.path.exists(product.video):
            os.remove(product.video)

        # Update fields if they are provided
        for field, value in product_update_data.dict(exclude_unset=True).items():
            setattr(product, field, value)

        # Handle file uploads
        if image_file:
            product.image = self.save_file(image_file, "images")
        if video_file:
            product.video = self.save_file(video_file, "videos")

        product.updated_at = datetime.now()
        session.commit()
        session.refresh(product)

        if product.image:
            product.image = f"https://api.toprateddesigner.com/{product.image}"
        if product.video:
            product.video = f"https://api.toprateddesigner.com/{product.video}"

        return product

    def delete_product(self, product_uid: uuid.UUID, session: Session):
        product = session.query(Products).filter(Products.uid == product_uid.bytes).first()
        if product:
            if product.image and os.path.exists(product.image):
                os.remove(product.image)
            if product.video and os.path.exists(product.video):
                os.remove(product.video)
            session.delete(product)
            session.commit()
            return True
        return False