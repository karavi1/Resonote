from flask import Flask
from app.routes.example import example_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    app.register_blueprint(example_bp, url_prefix="/api")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} -> {rule.rule}")

    return app