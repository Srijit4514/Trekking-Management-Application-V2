from modules import db, User
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"message": "Mission required data"}), 400
    
    user_name = User.query.filter_by(username=username).first()
    user_email = User.query.filter_by(email=email).first()

    if user_name or user_email:
        return jsonify({"message": "Username or email alredy exists!!"}), 400

    new_user = User(
        username=username, 
        email=email,
        password=generate_password_hash(password),
        role="users",
        is_active=True  
    ) 
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Account created successfully. Please login."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400
        
    this_user = User.query.filter_by(username=username).first()
    
    if not this_user or not check_password_hash(this_user.password, password):
        return jsonify({"message": "Invalid username or password."}), 401
        
    if not this_user.is_active:
        return jsonify({"message": "Your account is inactive. Please contact the administrator."}), 403

    if this_user.role == "user":
        this_user.role = "users"
        db.session.commit()

    effective_role = "users" if this_user.role in {"users", "user"} else this_user.role

    access_token = create_access_token(
        identity=str(this_user.id), 
        additional_claims={"role": effective_role, "username": this_user.username}
    )

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "role": effective_role,
        "username": this_user.username
    }), 200