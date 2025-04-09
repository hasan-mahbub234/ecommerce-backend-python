from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .model import Portfolios, PortfolioImage
from .schema import CreatePortfolio, UpdatePortfolio
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
import os
from typing import Optional, List
from ..blogs.service import BASE_URL
import cloudinary 
import cloudinary.uploader

cloudinary.config(
    cloud_name="ddacq5ltb",
    api_key="985616939343421",
    api_secret="oI07cgZ3rGa0VJ8DW354oQV013g"
)

class PortfolioService:
    def image_urls(self, portfolio: Portfolios):
        if portfolio.images:
            for img in portfolio.images:
                if not img.image_url.startswith("http"):
                    img.image_url = f"{BASE_URL}{img.image_url}"

    def get_all_portfolio(self, session: Session):
        statement = select(Portfolios).order_by(desc(Portfolios.created_at))
        result = session.execute(statement)
        portfolios = result.scalars().all()
        for portfolio in portfolios:
            self.image_urls(portfolio)
        return portfolios

    def get_singlePortfolio(self, portfolio_uid: uuid.UUID, session: Session):
        statement = select(Portfolios).where(Portfolios.uid == portfolio_uid.bytes)
        result = session.execute(statement)
        portfolio = result.scalar_one_or_none()
        if portfolio:
            self.image_urls(portfolio)
        return portfolio
    
    def save_images(self, images_files: List[UploadFile]) -> List[str]:
        """Save multiple images to Cloudinary and return URLs"""
        saved_urls = []
        for img in images_files:
            if img:
                try:
                    result = cloudinary.uploader.upload(
                        img.file,
                        folder="blog_images",
                        public_id=f"img_{uuid.uuid4().hex}",
                        resource_type="auto"
                    )
                    saved_urls.append(result['secure_url'])
                except Exception as e:
                    print(f"Error uploading image {img.filename}: {e}")
                    continue
        return saved_urls
    
    def create_portfolio(self, portfolio_data: CreatePortfolio, images_file: List[UploadFile], session: Session):
        new_portfolio = Portfolios(
            type= portfolio_data.type,
            title = portfolio_data.title,
            desc= portfolio_data.desc,
            tech= portfolio_data.tech
        )
        
        session.add(new_portfolio)
        session.commit()
        session.refresh(new_portfolio)

        if images_file:
            images_path = self.save_images(images_file)
            for img_path in images_path:
                portfolio_image = PortfolioImage(
                    image_url=img_path,
                    portfolio_uid=new_portfolio.uid
                )
                session.add(portfolio_image)
            session.commit()
            session.refresh(new_portfolio)

        self.image_urls(new_portfolio)
        return new_portfolio
    
    def update_portfolio(self, portfolio_uid: uuid.UUID, portfolio_update_data: UpdatePortfolio, 
                    images_file: List[UploadFile], session: Session):
        try:
            portfolio = session.query(Portfolios).filter(Portfolios.uid == portfolio_uid.bytes).first()
            if not portfolio:
                return None

            # Update basic fields
            for attr in ['type', 'title', 'desc', 'tech']:
                new_value = getattr(portfolio_update_data, attr, None)
                if new_value is not None:
                    setattr(portfolio, attr, new_value)

            # Handle images only if new ones are provided
            if images_file:  # Simplified check - empty list will skip this
                try:
                    # Delete old images if they exist
                    if portfolio.images:
                        for img in portfolio.images:
                            if os.path.exists(img.image_url):
                                os.remove(img.image_url)
                            session.delete(img)
                        session.flush()  # Flush deletes before adding new ones

                    # Save new images
                    images_path = self.save_images(images_file)
                    for img_path in images_path:
                        portfolio_image = PortfolioImage(
                            image_url=img_path,
                            portfolio_uid=portfolio.uid
                        )
                        session.add(portfolio_image)
                except Exception as e:
                    session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error updating images: {str(e)}"
                    )

            portfolio.updated_at = datetime.now()
            session.commit()
            session.refresh(portfolio)

            self.image_urls(portfolio)
            return portfolio
        except HTTPException:
            raise  # Re-raise HTTP exceptions
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating portfolio: {str(e)}"
            )
    
    def delete_portfolio(self, portfolio_uid: uuid.UUID, session: Session):
        portfolio = session.query(Portfolios).filter(Portfolios.uid == portfolio_uid.bytes).first()
        if portfolio:
            for img in portfolio.images:
                if os.path.exists(img.image_url):
                    os.remove(img.image_url)
                session.delete(img)

            session.delete(portfolio)
            session.commit()
            return True
        return False
