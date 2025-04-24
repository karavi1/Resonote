from flask import Flask
from flask_cors import CORS
from app.routes.core_routes import core_bp
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile("config.py")

    app.register_blueprint(core_bp, url_prefix="/api")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} -> {rule.rule}")

    return app