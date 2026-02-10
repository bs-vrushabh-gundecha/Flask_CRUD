from .extensions import db
from werkzeug.security  import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(300), nullable=True)
    contact = db.Column(db.String(13), nullable=True)

    def __repr__(self):
        return f"<User {self.name}>"


class AdminMaster(db.Model):
    __tablename__ = "admin_master"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=True)
    password = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(50), default="admin")

    def __repr__(self):
        return f"<AdminMaster {self.email}>"
