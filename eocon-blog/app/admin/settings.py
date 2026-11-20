from flask import Blueprint, request, jsonify
from app.auth.session import require_role
from app.db import get_db

settings_bp = Blueprint("settings", __name__, url_prefix="/api/admin")


@settings_bp.before_request
def check_settings_access():
    user = require_role("admin")
    if not user:
        return jsonify({"error": "Admin access required"}), 403


@settings_bp.route("/settings")
def get_settings():
    db = get_db()
    rows = db.execute("SELECT key, value FROM settings").fetchall()
    result = {row["key"]: row["value"] for row in rows}
    return jsonify(result)


@settings_bp.route("/settings", methods=["PUT"])
def update_settings():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    db = get_db()
    for key, value in data.items():
        db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, str(value))
        )
    db.commit()
    return jsonify({"message": "Settings updated"})
