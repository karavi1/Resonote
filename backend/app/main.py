from flask import Flask
from flask_cors import CORS
from app.routes.core_routes import core_bp
import os

if os.getenv("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    config_path = os.getenv("FLASK_CONFIG", "config.py")
    app.config.from_pyfile(config_path)

    app.register_blueprint(core_bp, url_prefix="/api")

    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} -> {rule.rule}")

    return app