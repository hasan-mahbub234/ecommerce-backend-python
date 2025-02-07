from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .models import Products
from .schemas import CreateProduct, UpdateProduct
import uuid
from datetime import datetime

class ProductService:
    def get_all_products(self, session: Session):
        statement = select(Products).order_by(desc(Products.created_at))
        result = session.execute(statement)
        return result.scalars().all()

    def get_product(self, product_uid: uuid.UUID, session: Session):
        statement = select(Products).where(Products.uid == product_uid.bytes)
        result = session.execute(statement)
        return result.scalar_one_or_none()

    def create_product(self, product_data: CreateProduct, session: Session):
        product_data_dict = product_data.model_dump()

        new_product = Products(**product_data_dict)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)  # Refresh to get updated instance

        return new_product

    def update_product(self, product_uid: uuid.UUID, product_update_data: UpdateProduct, session: Session):
        product = session.query(Products).filter(Products.uid == product_uid.bytes).first()
        if not product:
            return None

        for key, value in product_update_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        product.updated_at = datetime.now()

        session.commit()
        session.refresh(product)
        return product

    def delete_product(self, product_uid: uuid.UUID, session: Session):
        product = session.query(Products).filter(Products.uid == product_uid.bytes).first()
        if product:
            session.delete(product)
            session.commit()
            return True
        return False
