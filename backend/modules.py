from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="users") # admin, staff, or users
    is_active = db.Column(db.Boolean, default=True)   
    
    # Relationships
    bookings = db.relationship('Booking', back_populates='user', lazy=True)
    staff_profile = db.relationship('StaffProfile', backref='user', uselist=False)

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(110), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False) # Easy, Medium, Hard
    duration = db.Column(db.String(50), nullable=False)  
    slots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Open") 
    
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_staff = db.relationship('User', foreign_keys=[assigned_staff_id])
    
    bookings = db.relationship('Booking', backref='trek', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    booking_status = db.Column(db.String(20), default="Booked") # Booked / Cancelled / Completed
    payment_status = db.Column(db.String(20), default="Paid")
    
    user = db.relationship('User', foreign_keys=[user_id], back_populates='bookings') 

class StaffProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_number = db.Column(db.Integer, nullable=True)