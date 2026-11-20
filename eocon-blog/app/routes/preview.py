from flask import Blueprint, request, jsonify
from app.services.templating import process_template

preview_bp = Blueprint("preview", __name__)


@preview_bp.route("/api/preview", methods=["POST"])
def preview():
    data = request.get_json()
    if not data or "body" not in data:
        return jsonify({"error": "Missing body"}), 400
    body = data["body"]
    result = process_template(body)
    return jsonify({"rendered": result})
