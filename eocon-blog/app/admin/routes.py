import os
from flask import Blueprint, jsonify
from app.auth.session import require_role
from app.db import get_db
from app.models.user import list_users

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.before_request
def check_admin():
    user = require_role("admin")
    if not user:
        return jsonify({"error": "Admin access required"}), 403


@admin_bp.route("/users")
def admin_users():
    users = list_users()
    return jsonify({"users": [dict(u) for u in users]})


@admin_bp.route("/stats")
def admin_stats():
    db = get_db()
    posts = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    comments = db.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
    users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    return jsonify({"posts": posts, "comments": comments, "users": users})


@admin_bp.route("/purge-cache", methods=["POST"])
def purge_cache():
    return jsonify({"message": "Cache purged"})


@admin_bp.route("/system")
def system_info():
    hostname = os.popen("hostname").read().strip()
    return jsonify({"hostname": hostname})
