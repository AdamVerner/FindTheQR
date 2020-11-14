import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def get_log_file(app) -> str:
    """If not LOG_PATH is set, create directory logs and use that"""
    if not app.config.get("LOG_PATH") and not os.path.exists("logs"):
        os.mkdir("logs")

    return app.config.get("LOG_PATH") or "logs/NetioCloud.log"


def create_app():
    app = Flask(__name__)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.engine.dispose()

        migrate.init_app(app, db)

    from app.routes import bp as main_bp

    app.register_blueprint(main_bp)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Netio Cloud startup")

    return app