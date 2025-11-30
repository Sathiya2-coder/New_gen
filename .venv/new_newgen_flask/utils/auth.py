from werkzeug.security import check_password_hash, generate_password_hash
from models.database import User, db

def init_admin_user():
    """Initialize admin user if not exists"""
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password=generate_password_hash('nec123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin/nec123")

def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None