from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from app.db.models import Registration
from app.schemas.registration import RegistrationCreate


def create_booking(db: Session, booking_data: RegistrationCreate):
    overlapping = db.query(Registration).filter(
        and_(
            Registration.place == booking_data.place,
            Registration.start_time < booking_data.end_time,
            Registration.end_time > booking_data.start_time
        )
    ).first()

    if overlapping:
        raise ValueError("Это место уже занято в это время")

    booking = Registration(**booking_data.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_user_bookings(db: Session, username: str):
    return db.query(Registration).filter(Registration.username == username).all()


def cancel_booking(db: Session, booking_id: int):
    booking = db.query(Registration).filter(Registration.id == booking_id).first()
    if not booking:
        return None
    db.delete(booking)
    db.commit()
    return booking


def get_free_places(db: Session, start: datetime, end: datetime):
    busy_places = db.query(Registration.place).filter(
        and_(
            Registration.start_time <= end,
            Registration.end_time >= start
        )
    ).all()
    busy_set = set(place for (place,) in busy_places)

    rows = "ABCDEFGH"
    columns = range(1, 9)
    all_places = [f"{row}{col}" for row in rows for col in columns]

    free = [p for p in all_places if p not in busy_set]
    return free
