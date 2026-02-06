from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(300), nullable=True)
    contact = db.Column(db.String(13), nullable=True)

    def __repr__(self):
        return f"<User {self.name}>"
