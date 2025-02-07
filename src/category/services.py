from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .models import Categories
from .schemas import CreateCategories, UpdateCategories
import uuid
from datetime import datetime

class CategoriesService:
    def get_all_categories(self, session: Session):
        statement = select(Categories).order_by(desc(Categories.created_at))
        result = session.execute(statement)
        return result.scalars().all()

    def get_category(self, category_uid: uuid.UUID, session: Session):
        statement = select(Categories).where(Categories.uid == category_uid.bytes)
        result = session.execute(statement)
        return result.scalar_one_or_none()

    def create_category(self, category_data: CreateCategories, session: Session):
        category_data_dict = category_data.model_dump()

        new_category = Categories(**category_data_dict)
        session.add(new_category)
        session.commit()
        session.refresh(new_category)  # Refresh to get updated instance

        return new_category

    def update_category(self, category_uid: uuid.UUID, category_update_data: UpdateCategories, session: Session):
        category = session.query(Categories).filter(Categories.uid == category_uid.bytes).first()
        if not category:
            return None

        for key, value in category_update_data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        category.updated_at = datetime.now()

        session.commit()
        session.refresh(category)
        return category

    def delete_category(self, category_uid: uuid.UUID, session: Session):
        category = session.query(Categories).filter(Categories.uid == category_uid.bytes).first()
        if category:
            session.delete(category)
            session.commit()
            return True
        return False
