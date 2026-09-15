from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from modules import db, User, Trek, Booking
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user", __name__)

@user_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def user_dashboard():
    claims = get_jwt()
    if claims.get("role") not in {"users", "user"}:
        return jsonify({"error": "Access denied. Registered users only."}), 403
    
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(current_user_id)

    loc_query = request.args.get("location", "").strip()
    diff_query = request.args.get("difficulty", "").strip()
    dur_query = request.args.get("duration", "").strip()

    query = Trek.query.filter_by(status="Open")
    if loc_query:
        query = query.filter(Trek.location.ilike(f"%{loc_query}%"))
    if diff_query:
        query = query.filter_by(difficulty=diff_query)
    if dur_query:
        query = query.filter(Trek.duration.ilike(f"%{dur_query}%"))

    available_treks = query.all()

    user_booings = Booking.query.filter_by(user_id=current_user_id).all()

    return jsonify({
        "user_profile": {
            "username": user.username,
            "email": user.email
        },
        "available_treks": [{
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "difficulty": t.difficulty,
            "duration": t.duration,
            "slots": t.slots,
            "start_date": t.start_date.isoformat(),
            "end_date": t.end_date.isoformat(),
            "price": t.price
        } for t in available_treks],
        "bookings": [{
            "id": b.id,
            "trek_name": b.trek.name,
            "location": b.trek.location,
            "duration": b.trek.duration,
            "start_date": b.trek.start_date.isoformat(),
            "booking_status": b.booking_status,
            "payment_status": b.payment_status
        } for b in user_booings]
    }), 200

@user_bp.route("/trek/book/<int:trek_id>", methods=["POST"])
@jwt_required()
def book_trek(trek_id):
    claims = get_jwt()
    if claims.get("role") not in {"users", "user"}:
        return jsonify({"error": "Access denied."}), 403
    
    current_user_id = int(get_jwt_identity())
    trek = Trek.query.get_or_404(trek_id)

    if trek.slots <= 0 or trek.status != "Open":
        return jsonify({"error": "This expedition is full or closed for registrations."}), 400
    
    existing = Booking.query.filter_by(user_id=current_user_id, trek_id=trek_id, booking_status="Booked").first()
    if existing:
        return jsonify({"error": "You are alredy registered for thie trek."}), 400
    
    new_booking = Booking(
        user_id=current_user_id,
        trek_id=trek.id,
        booking_status="Booked",
        payment_status="Paid"
    )
    trek.slots -= 1

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": f"Successfully joined the '{trek.name}' crew!"}), 201

@user_bp.route("/profile/update", methods=["POST"])
@jwt_required()
def update_profile():
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(current_user_id)
    data = request.get_json() or {}

    username_input = data.get("username")
    email_input = data.get("email")
    password_input = data.get("password")

    if username_input:
        user.username = username_input
    if email_input:
        user.email = email_input
    if password_input:
        user.password = generate_password_hash(password_input)

    db.session.commit()
    return jsonify({"message": "Profile configurations saved successfully."}), 200