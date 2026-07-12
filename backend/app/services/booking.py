from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from app.models.booking import Booking
from app.models.asset import Asset
from app.schemas.booking import BookingCreate

def get_booking_by_id(db: Session, booking_id: int) -> Optional[Booking]:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def list_bookings(
    db: Session,
    asset_id: Optional[int] = None,
    user_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Booking]:
    query = db.query(Booking)
    if asset_id is not None:
        query = query.filter(Booking.asset_id == asset_id)
    if user_id is not None:
        query = query.filter(Booking.user_id == user_id)
    if status_filter is not None:
        query = query.filter(Booking.status == status_filter)
    return query.offset(skip).limit(limit).all()

def create_booking(db: Session, booking_in: BookingCreate, user_id: int) -> Booking:
    # 1. Validate Asset exists
    asset = db.query(Asset).filter(Asset.id == booking_in.asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset/Resource with ID {booking_in.asset_id} not found"
        )

    # 2. Check if asset can be booked (not under maintenance or retired)
    if asset.status in ["Under Maintenance", "Retired"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot book asset with status '{asset.status}'"
        )

    # 3. Check for overlapping bookings
    # Overlap exists if: (start_A < end_B) AND (end_A > start_B)
    overlap = db.query(Booking).filter(
        and_(
            Booking.asset_id == booking_in.asset_id,
            Booking.status == "Approved",
            Booking.start_time < booking_in.end_time,
            Booking.end_time > booking_in.start_time
        )
    ).first()

    if overlap:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Asset is already booked during the selected time period"
        )

    # 4. Create booking
    db_booking = Booking(
        asset_id=booking_in.asset_id,
        user_id=user_id,
        start_time=booking_in.start_time,
        end_time=booking_in.end_time,
        purpose=booking_in.purpose,
        status="Approved"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def cancel_booking(db: Session, booking_id: int, current_user_id: int, user_role: str) -> Booking:
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID {booking_id} not found"
        )

    if db_booking.status == "Cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )

    # Permission check: User who created booking OR Admin/Asset Manager can cancel
    if db_booking.user_id != current_user_id and user_role not in ["Admin", "Asset Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to cancel this booking"
        )

    db_booking.status = "Cancelled"
    db.commit()
    db.refresh(db_booking)
    return db_booking