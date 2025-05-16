from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.registration import RegistrationCreate
from app.services.booking_service import create_booking, get_user_bookings, \
    cancel_booking, get_free_places
from datetime import datetime

booking_router = Blueprint("booking", __name__, url_prefix="/api/bookings")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@booking_router.route("/", methods=["POST"])
def book_place():
    data = request.json
    try:
        booking_data = RegistrationCreate(**data)
    except Exception as e:
        return jsonify({"error": f"Invalid input: {e}"}), 400

    db = next(get_db())
    try:
        booking = create_booking(db, booking_data)
        return jsonify({"message": "Booking created", "id": booking.id})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@booking_router.route("/<username>", methods=["GET"])
def get_bookings(username):
    db = next(get_db())
    bookings = get_user_bookings(db, username)
    return jsonify([{
        "id": b.id,
        "place": b.place,
        "start_time": b.start_time.isoformat(),
        "end_time": b.end_time.isoformat()
    } for b in bookings])


@booking_router.route("/cancel/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    db = next(get_db())
    result = cancel_booking(db, booking_id)
    if result:
        return jsonify({"message": "Booking cancelled"})
    return jsonify({"error": "Booking not found"}), 404


@booking_router.route("/free", methods=["GET"])
def free_places():
    try:
        start = datetime.fromisoformat(request.args.get("start"))
        end = datetime.fromisoformat(request.args.get("end"))
    except Exception:
        return jsonify({"error": "Invalid datetime format. Use ISO 8601."}), 400

    db = next(get_db())
    free = get_free_places(db, start, end)
    return jsonify({"free_places": free})
