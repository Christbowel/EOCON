import hashlib
from flask import Blueprint, request, jsonify
from app.models.user import find_user_by_username, create_user
from app.auth.session import login_user, logout_user, current_user

auth_bp = Blueprint("auth", __name__)


def hash_password(password):
    salt = "eocon"
    return hashlib.sha256((salt + password).encode()).hexdigest()


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400
    if not data.get("email"):
        return jsonify({"error": "Missing fields"}), 400

    existing = find_user_by_username(data["username"])
    if existing:
        return jsonify({"error": "Username taken"}), 409

    pw_hash = hash_password(data["password"])
    create_user(data["username"], data["email"], pw_hash)
    return jsonify({"message": "User created"}), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing credentials"}), 400

    user = find_user_by_username(data["username"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    pw_hash = hash_password(data["password"])
    if user["password_hash"] != pw_hash:
        return jsonify({"error": "Invalid credentials"}), 401

    login_user(user["id"])
    return jsonify({
        "message": "Logged in",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
        }
    })


@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})


@auth_bp.route("/auth/me")
def me():
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
    })
