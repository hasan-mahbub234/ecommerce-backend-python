from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from .service import PortfolioService
from .schema import CreatePortfolio, UpdatePortfolio, Portfolio
from typing import List, Optional
import uuid

portfolio_router = APIRouter()
portfolio_service = PortfolioService()

@portfolio_router.get("/", response_model=List[Portfolio])
def all_portfolios(session: Session = Depends(get_session)):
    portfolios = portfolio_service.get_all_portfolio(session)
    return portfolios


@portfolio_router.post("/", response_model=Portfolio, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    type: str = Form(...),
    title: str = Form(...),
    desc: str = Form(...),
    tech: str = Form(...),
    images_file: List[UploadFile] = File([]),
    session: Session = Depends(get_session)
):
    # Properly split and clean the tech string
    tech_list = [t.strip() for t in tech.split(",") if t.strip()] if tech else []
    
    portfolio_data = CreatePortfolio(
        type=type,
        title=title,
        desc=desc,
        tech=tech_list
    )
    new_portfolio = portfolio_service.create_portfolio(portfolio_data, images_file, session)
    if not new_portfolio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create portfolio"
        )
    return new_portfolio


@portfolio_router.get("/{portfolio_uid}", response_model=Portfolio)
def single_portfolio(portfolio_uid: uuid.UUID, session: Session = Depends(get_session)):
    portfolio = portfolio_service.get_singlePortfolio(portfolio_uid, session)
    if portfolio:
        return portfolio
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Portfolio not found"
    )


@portfolio_router.patch("/{portfolio_uid}", response_model=Portfolio)
def update_portfolio(
    portfolio_uid: uuid.UUID,
    type: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    desc: Optional[str] = Form(None),
    tech: Optional[str] = Form(None),
    images_file: Optional[List[UploadFile]] = File(None),  # Make it Optional
    session: Session = Depends(get_session)
):
    # Convert tech string to list if provided
    tech_list = None
    if tech is not None:
        tech_list = [t.strip() for t in tech.split(",") if t.strip()]
    
    # Create update data with only provided fields
    update_data = {}
    if type is not None:
        update_data['type'] = type
    if title is not None:
        update_data['title'] = title
    if desc is not None:
        update_data['desc'] = desc
    if tech_list is not None:
        update_data['tech'] = tech_list
    
    portfolio_update_data = UpdatePortfolio(**update_data)
    
    # Convert None to empty list if no files provided
    images_to_update = images_file if images_file is not None else []
    
    try:
        updated_portfolio = portfolio_service.update_portfolio(
            portfolio_uid, portfolio_update_data, images_to_update, session
        )
        if updated_portfolio:
            return updated_portfolio
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )


@portfolio_router.delete("/{portfolio_uid}")
def delete_portfolio(portfolio_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = portfolio_service.delete_portfolio(portfolio_uid, session)
    if deleted:
        return {"message": "Portfolio deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Portfolio not found"
    )