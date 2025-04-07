from flask import Blueprint, jsonify
try:
    from app.services.ingestion.reuters_scraper import ReutersScraper
except Exception as e:
    print("Error importing ReutersScraper:", e)

print("Example routes loaded")

example_bp = Blueprint("example", __name__)

@example_bp.route("/ingest/reuters", methods=["GET"])
def ingest_reuters():
    scraper = ReutersScraper(headless=True)
    try:
        results = scraper.ingest(max_count=5)
        return jsonify(results) # Access at http://localhost:5000/api/ingest/reuters
    finally:
        scraper.close()

@example_bp.route("/hello")
def hello():
    return "Hello from blueprint!" # Access at http://localhost:5000/api/hello