from flask import Blueprint, jsonify

example_bp = Blueprint("example", __name__)

@example_bp.route("/", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello from Resonote backend!"})