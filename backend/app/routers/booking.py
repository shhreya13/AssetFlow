from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.routers.dependencies import get_current_user
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingOut
from app.schemas.response import ApiResponse, success_response
import app.services.booking as booking_service

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=ApiResponse[BookingOut], status_code=status.HTTP_201_CREATED)
def book_resource(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = booking_service.create_booking(db, booking_in, current_user.id)
    return success_response(
        message="Resource booked successfully",
        data=BookingOut.model_validate(booking)
    )

@router.get("/", response_model=ApiResponse[List[BookingOut]])
def get_all_bookings(
    asset_id: Optional[int] = Query(None, description="Filter by Asset ID"),
    user_id: Optional[int] = Query(None, description="Filter by User ID who booked"),
    status: Optional[str] = Query(None, description="Filter by status (Approved, Cancelled)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = booking_service.list_bookings(
        db, 
        asset_id=asset_id, 
        user_id=user_id, 
        status_filter=status, 
        skip=skip, 
        limit=limit
    )
    data = [BookingOut.model_validate(b) for b in bookings]
    return success_response(
        message="Bookings retrieved successfully",
        data=data
    )

@router.get("/{id}", response_model=ApiResponse[BookingOut])
def get_booking_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = booking_service.get_booking_by_id(db, id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking record with ID {id} not found"
        )
    return success_response(
        message="Booking record retrieved successfully",
        data=BookingOut.model_validate(booking)
    )

@router.post("/{id}/cancel", response_model=ApiResponse[BookingOut])
def cancel_existing_booking(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = booking_service.cancel_booking(db, id, current_user.id, current_user.role)
    return success_response(
        message="Booking cancelled successfully",
        data=BookingOut.model_validate(booking)
    )