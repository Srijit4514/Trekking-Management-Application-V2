import io
from flask import Blueprint, request, jsonify, session, send_file
from fpdf import FPDF
from modules import db, User, Trek, Booking
from datetime import datetime
from sqlalchemy import func
from tasks import send_staff_credentials_email
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    claims = get_jwt() 
    if claims.get("role") != "admin":
        return jsonify({"error": "Access denied. Authorized administrators only."}), 403

    search_query = request.args.get("search", "").strip()

    users_query = User.query.filter(User.role.in_(["users", "user"]))
    staff_query = User.query.filter(User.role == "staff")
    treks_query = Trek.query
    bookings_data = Booking.query.all()

    
    if search_query:
        if search_query.isdigit():
            search_id = int(search_query)
            users_query = users_query.filter(User.id == search_id)
            staff_query = staff_query.filter(User.id == search_id)
            treks_query = treks_query.filter(Trek.id == search_id)
        else:
            users_query = users_query.filter(User.username.contains(search_query))
            staff_query = staff_query.filter(User.username.contains(search_query))
            treks_query = treks_query.filter(Trek.name.contains(search_query))

    users_data = users_query.all()
    staff_data = staff_query.all()
    treks_data = treks_query.all()

    analytics_raw = db.session.query(
        Trek.name,
        func.count(Booking.id).label("total_bookings"),
        func.sum(Trek.price).label("total_revenue")
    ).join(Booking, Booking.trek_id == Trek.id) .filter(Booking.booking_status != "Cancelled") .group_by(Trek.id).all()

    analytics_data = [{
        "trek_name": row.name,
        "total_bookings": row.total_bookings,
        "revenue": float(row.total_revenue) if row.total_revenue else 0.0
    } for row in analytics_raw]

    total_revenue = sum(item["revenue"] for item in analytics_data)

    total_treks = len(treks_data)
    total_users = len(users_data)
    total_staff = len(staff_data)
    total_bookings = len(bookings_data)

    return jsonify({
        "metrics": {
            "totalTreks": total_treks,
            "totalUsers": total_users,
            "totalStaff": total_staff,
            "totalBookings": total_bookings,
            "totalRevenue": total_revenue
        },
        "analytics": analytics_data,
        "treks": [{
            "id": t.id,
            "name": t.name,
            "difficulty": t.difficulty,
            "duration": t.duration,
            "slots": t.slots,
            "location": t.location,
            "start_date": t.start_date.strftime("%Y-%m-%d") if t.start_date else None,
            "end_date": t.end_date.strftime("%Y-%m-%d") if t.end_date else None,
            "price": t.price,
            "assigned_staff": {
                "id": t.assigned_staff.id,
                "username": t.assigned_staff.username
            } if t.assigned_staff else None
        } for t in treks_data],
        "users": [{
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_active": u.is_active
        } for u in users_data],
        "staff": [{
            "id": s.id,
            "username": s.username,
            "email": s.email,
            "is_active": s.is_active
        } for s in staff_data],
        "bookings": [{
            "id": b.id,
            "booking_status": b.booking_status,
            "payment_status": b.payment_status,
            "user": {"username": b.user.username} if b.user else None,
            "trek": {"id": b.trek.id, "name": b.trek.name} if b.trek else None
        } for b in bookings_data]
    }), 200


@admin_bp.route("/staff/add", methods=["POST"])
@jwt_required()
def add_staff():

    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized Access"}), 401

    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"error": "Missing mandatory field parameters"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "Username or Email already registered!"}), 409
        
    new_staff = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role="staff",
        is_active=True
    )
    db.session.add(new_staff)
    db.session.commit()
    
    send_staff_credentials_email.delay(email, username, password)

    return jsonify({"message": f"Staff member '{username}' successfully added."}), 201


@admin_bp.route("/user/toggle_status/<int:user_id>", methods=["POST"])
@jwt_required()
def toggle_status(user_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized Access"}), 401

    target_user = User.query.get_or_404(user_id)
    target_user.is_active = not target_user.is_active
    db.session.commit()

    status_txt = "activated" if target_user.is_active else "blacklisted/deactivated"
    return jsonify({
        "message": f"'{target_user.username}' has been successfully {status_txt}.",
        "is_active": target_user.is_active
    }), 200


@admin_bp.route("/trek/add", methods=["POST"])
@jwt_required()
def add_trek():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized Access"}), 401

    data = request.get_json() or {}
    name = data.get("name")
    difficulty = data.get("difficulty")
    location = data.get("location")

    raw_start = data.get("start_date")
    raw_end = data.get("end_date")

    slots = int(data.get("slots", 0))

    try: 
        price = float(data.get("price", 0.0))
    except (ValueError, TypeError):
        price = 0.0

    try:
        start_date = datetime.strptime(raw_start, "%Y-%m-%d").date()
        end_date = datetime.strptime(raw_end, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid date format!"}), 400
    
    if end_date < start_date:
        return jsonify({"error": "End date cannot be before start date!"}), 400
    
    days_count = (end_date - start_date).days + 1
    duration = f"{days_count} Days"

    new_trek = Trek(
        name=name,
        difficulty=difficulty,
        duration=duration,
        slots=slots,
        location=location,
        start_date=start_date,
        end_date=end_date,
        price=price,
        status="Upcoming"
    )
    db.session.add(new_trek)
    db.session.commit()
    
    return jsonify({"message": f"Trek route '{name}' created successfully."}), 201


@admin_bp.route("/trek/edit/<int:trek_id>", methods=["PUT", "POST"])
@jwt_required()
def edit_trek(trek_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized Access"}), 401

    trek = Trek.query.get_or_404(trek_id)
    data = request.get_json() or {}

    trek.name = data.get("name", trek.name)
    trek.difficulty = data.get("difficulty", trek.difficulty)
    trek.location = data.get("location", trek.location)
    trek.slots = int(data.get("slots", trek.slots))
    trek.status = data.get("status", trek.status or "Upcoming")
    
    try: 
        if "price" in data:
            trek.price = float(data.get("price"))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid price format!"}), 400

    try:
        if data.get("start_date"):
            trek.start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
        if data.get("end_date"):
            trek.end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid date format!"}), 400
    
    if trek.end_date < trek.start_date:
        return jsonify({"error": "End date cannot be before start date!"}), 400

    days_count = (trek.end_date - trek.start_date).days + 1
    trek.duration = f"{days_count} Days"
    
    db.session.commit()
    return jsonify({"message": "Trek details modified successfully."}), 200

@admin_bp.route("/trek/assign_staff", methods=["POST"])
@jwt_required()
def assign_staff():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized Access"}), 401

    data = request.get_json() or {}
    trek_id = data.get("trek_id")
    staff_id = data.get("staff_id")

    trek = Trek.query.get_or_404(trek_id)
    
    if not staff_id:
        trek.assigned_staff_id = None
        message = "Staff unassigned from this trek successfully."
    else:
        trek.assigned_staff_id = int(staff_id)
        message = "Staff assigned successfully to the trek."

    db.session.commit()
    return jsonify({"message": message}), 200

@admin_bp.route("/trek/<int:trek_id>/booking_report", methods=["GET"])
@jwt_required()
def generate_trek_report(trek_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Access denied. Authorized administrators only."}), 403

    trek = Trek.query.get_or_404(trek_id)
    bookings = Booking.query.filter_by(trek_id=trek_id).all()

    total_bookings = len(bookings)
    total_revenue = sum(trek.price for b in bookings if b.payment_status == "Paid")

    pdf = FPDF()
    pdf.add_page()
 
    pdf.set_font("Arial", "B", 16)
    
    pdf.cell(190, 10, txt=f"Trekking Report: {str(trek.name)}", ln=1, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 8, txt=f"Location: {str(trek.location)}", ln=1)
    pdf.cell(190, 8, txt=f"Total Slots: {str(trek.slots)}", ln=1)
    pdf.cell(190, 8, txt=f"Total Bookings placed: {str(total_bookings)}", ln=1)
    pdf.cell(190, 8, txt=f"Total Estimated Revenue: ${total_revenue:.2f}", ln=1)
    pdf.ln(10)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 8, txt="Booking Details", ln=1)
    pdf.ln(2)

    pdf.set_font("Arial", style="B", size=10)
    col_widths = [15, 50, 40, 40]
    pdf.cell(col_widths[0], 8, txt="ID", border=1, align="C")
    pdf.cell(col_widths[1], 8, txt="Trekker Name", border=1, align="C")
    pdf.cell(col_widths[2], 8, txt="Booking Status", border=1, align="C")
    pdf.cell(col_widths[3], 8, txt="Payment Status", border=1, align="C", ln=1)

    pdf.set_font("Arial", size=9)
    for b in bookings:
        username = b.user.username if b.user else "N/A"
        pdf.cell(col_widths[0], 8, txt=str(b.id), border=1, align="C")
        pdf.cell(col_widths[1], 8, txt=str(username), border=1, align="L")
        pdf.cell(col_widths[2], 8, txt=str(b.booking_status), border=1, align="C")
        pdf.cell(col_widths[3], 8, txt=str(b.payment_status), border=1, align="C", ln=1)

    pdf_buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S')
    
    if isinstance(pdf_output, str):
        pdf_buffer.write(pdf_output.encode('latin-1'))
    else:
        pdf_buffer.write(pdf_output)
    
    pdf_buffer.seek(0)

    response = send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"trek_{trek_id}_report.pdf"
    )
    
    return response

@admin_bp.route("/trek/delete/<int:trek_id>", methods=["POST", "DELETE"])
@jwt_required()
def remove_trek(trek_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized Access"}), 401

    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    
    return jsonify({"message": "Trek was successfully removed from listings."}), 200


@admin_bp.route('/logout', methods=["POST"])
@jwt_required()
def admin_logout():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized Access"}), 401
    session.clear()
    return jsonify({"message": "Logged out successfully from session context."}), 200