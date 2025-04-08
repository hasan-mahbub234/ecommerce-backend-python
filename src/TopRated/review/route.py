from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.db.database import get_session
from .service import ReviewService
from .schema import CreateReview, UpdateReview, Review
from typing import List, Optional
import uuid
from fastapi.responses import FileResponse
import os

review_router = APIRouter()
review_service = ReviewService()

@review_router.get("/", response_model=List[Review])
def all_reviews(session: Session = Depends(get_session)):
    reviews = review_service.get_all_review(session)
    return reviews

@review_router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
def create_expert(
    name: str = Form(...),
    review: str = Form(...),
    position: str = Form(...),
    image_file: UploadFile = File(),
    session: Session = Depends(get_session)
):
    review_data = CreateReview(
        name=name, review=review, position=position, 
    )
    new_review = review_service.create_review(review_data, image_file, session)

    return new_review


@review_router.get("/{review_uid}", response_model=Review)
def single_review(review_uid: uuid.UUID, session: Session = Depends(get_session)):
    review = review_service.get_singleReview(review_uid, session)
    if review:
        return review
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Review not found"
    )

@review_router.patch("/{review_uid}", response_model=Review)
def update_review(
    review_uid: uuid.UUID,
    name: Optional[str] = Form(None),
    review: Optional[str] = Form(None),
    position: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):
    update_data = {}
    if name is not None:
        update_data['name'] = name
    if review is not None:
        update_data['review'] = review
    if position is not None:
        update_data['position'] = position
    
    review_update_data = UpdateReview(**update_data)
    
    updated_review = review_service.update_review(
        review_uid, review_update_data, image_file, session
    )
    if updated_review:
        return updated_review
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Review not found"
    )

@review_router.delete("/{review_uid}",)
def delete_review(review_uid: uuid.UUID, session: Session = Depends(get_session)):
    deleted = review_service.delete_review(review_uid, session)
    if deleted:
        return {"message": "Review deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
