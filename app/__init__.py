from flask import Flask

from app.models import db
from config import Config
from app.blueprints.category import categories


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

        app.register_blueprint(categories)

    return app
