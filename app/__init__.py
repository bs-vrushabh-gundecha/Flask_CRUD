from flask import Flask
from .extensions import db, migrate
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .users.routes import users_bp
    from .auth.routes import auth_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)

    return app