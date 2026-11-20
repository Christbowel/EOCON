import re
from flask import Blueprint, request, jsonify
from app.auth.session import require_role

console_bp = Blueprint("console", __name__, url_prefix="/api/admin")

SAFE_EXPR = re.compile(r"^[\d\s\+\-\*/\(\)\.]+$")


@console_bp.before_request
def check_console_access():
    user = require_role("admin")
    if not user:
        return jsonify({"error": "Admin access required"}), 403


@console_bp.route("/console", methods=["POST"])
def run_console():
    token = request.headers.get("X-Admin-Token", "")
    if token != "eo-admin-7q3w9p":
        return jsonify({"error": "Invalid admin token"}), 403

    data = request.get_json()
    if not data or "expr" not in data:
        return jsonify({"error": "Missing expression"}), 400

    expr = data["expr"]
    if not SAFE_EXPR.match(expr):
        return jsonify({"error": "Expression not allowed"}), 400

    result = eval(expr)
    return jsonify({"result": result})
