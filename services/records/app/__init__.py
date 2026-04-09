from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("RECORDS_DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.patients import patients_bp
    from app.routes.records import records_bp

    app.register_blueprint(patients_bp, url_prefix="/api/patients")
    app.register_blueprint(records_bp, url_prefix="/api/records")

    return app