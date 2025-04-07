from flask import Flask
from app.routes.example import example_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    app.register_blueprint(example_bp, url_prefix="/api")

    return app