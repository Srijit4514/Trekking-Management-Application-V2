import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from modules import db, User
from werkzeug.security import generate_password_hash
from auth import auth_bp
from admin.admin_dashboard import admin_bp  
from staff.staff_dashboard import staff_bp  
from user.user_dashboard import user_bp
from tasks import celery_app          

app = Flask(__name__)
load_dotenv()
CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL")}})

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
jwt = JWTManager(app)

celery_app.conf.update(
    broker_url=os.environ.get("REDIS_URL"),
    result_backend=os.environ.get("REDIS_URL")
)
class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
celery_app.Task = ContextTask

with app.app_context():
    db.create_all()

    admin_user = User.query.filter_by(role="admin").first()
    if not admin_user:
        default_admin = User(
            username=os.getenv("ADMIN_USERNAME"),
            email="admin@example.com",
            password=generate_password_hash(os.getenv("ADMIN_PASSWORD")),
            role="admin",
            is_active=True
        )
        db.session.add(default_admin)
        db.session.commit()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")  
app.register_blueprint(staff_bp, url_prefix="/staff")
app.register_blueprint(user_bp, url_prefix="/user")

if __name__=="__main__":   
    app.run(debug=True, host="0.0.0.0", port=5001)