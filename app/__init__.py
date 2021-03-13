import os
import logging
from datetime import datetime
from random import getrandbits

from flask import Flask
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
auth = BasicAuth()


def create_app():
    app = Flask(__name__)

    if not os.path.exists('./app_secret.txt'):
        with open('./app_secret.txt', 'w') as f:
            f.write(str(getrandbits(64)))

    if app.debug:
        print('setting weak password for development')
        app.secret_key = 'SuperSecret'

    app.secret_key = open('./app_secret.txt').read() if not app.debug else 'SuperSecret'
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///../app.db')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config.setdefault('BASIC_AUTH_USERNAME', 'admin')
    app.config.setdefault('BASIC_AUTH_PASSWORD', 'admin')
    app.config.setdefault('END_DATE', '2021-03-14T20:00:00+01:00')

    db.init_app(app)
    auth.init_app(app)

    with app.app_context():
        db.create_all()
        db.engine.dispose()
        migrate.init_app(app, db)

    from app.routes import bp as main_bp
    from app.routes import admin_bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/secret')

    def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
        return value.strftime(format)

    app.add_template_filter(datetimeformat, 'datetimeformat')
    app.add_template_filter(datetime.fromisoformat, 'iso8601_to_time')

    app.add_template_global(app.config.get('END_DATE'), 'end_date')

    app.logger.setLevel(logging.DEBUG)

    return app
