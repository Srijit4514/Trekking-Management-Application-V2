from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity 
from modules import db, Trek

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():
    claims = get_jwt()
    if claims.get("role") != "staff":
        return jsonify({"error": "Access denied. Staff only."}), 403
    
    current_staff_id = get_jwt_identity()

    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_staff_id).all()

    treks_data = []
    for trek in assigned_treks:
        bookings_data = []
        for booking in trek.bookings:
            bookings_data.append({
                "id": booking.id,
                "booking_status": booking.booking_status,
                "payment_status": booking.payment_status,
                "user": {
                    "id": booking.user.id if booking.user else None,
                    "username": booking.user.username if booking.user else "Unknown user"
                }
            })
            
        treks_data.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "slots": trek.slots,
            "start_date": trek.start_date.isoformat() if trek.start_date else None, # Format dates safely for JSON
            "end_date": trek.end_date.isoformat() if trek.end_date else None,
            "price": trek.price,
            "status": trek.status,
            "bookings": bookings_data
        })
        
    return jsonify({
        "username": claims.get("username", "Staff Member"),
        "treks": treks_data
    }), 200

@staff_bp.route("/trek/update/<int:trek_id>", methods=["POST"])
@jwt_required()
def update_trek(trek_id):
    claims = get_jwt()
    if claims.get("role") != "staff":
        return jsonify({"error": "Access denied. Staff only."}), 403

    trek = Trek.query.get_or_404(trek_id)
    
    current_user_id = int(get_jwt_identity())
    if trek.assigned_staff_id != current_user_id:
        return jsonify({"error": "Access Denied. You are not assigned to this expedition."}), 403

    data = request.get_json() or {}
    
    slots = data.get("slots")
    new_status = data.get("status") 

    if slots is not None:
        trek.slots = int(slots)

    if new_status:
        if new_status == "Completed":
            trek.status = "Completed"
            for booking in trek.bookings:
                if booking.booking_status == "Booked":
                    booking.booking_status = "Completed"
        else:
            trek.status = new_status

    db.session.commit()
    
    return jsonify({
        "message": f"Parameters updated successfully. Status is now '{trek.status}'.",
        "trek": {
            "id": trek.id,
            "slots": trek.slots,
            "status": trek.status
        }
    }), 200

@staff_bp.route("/logout", methods=["POST"])
@jwt_required()
def staff_logout():
    claims = get_jwt()
    if claims.get("role") != "staff":
        return jsonify({"error": "Unauthorized Access"}), 401
    session.clear()
    return jsonify({"message": "Staff logged out successfully."}), 200