from flask import Blueprint, request, jsonify
from app.models.user import find_user_by_token
from app.models.post import get_published_posts, create_post
from app.lib.slugify import make_slug

api_bp = Blueprint("api_tokens", __name__)


def authenticate_token():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth[7:]
    return find_user_by_token(token)


@api_bp.route("/api/v1/posts")
def api_list_posts():
    user = authenticate_token()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    posts = get_published_posts(limit=50)
    return jsonify({"posts": [dict(p) for p in posts]})


@api_bp.route("/api/v1/posts", methods=["POST"])
def api_create_post():
    user = authenticate_token()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    if user["role"] not in ("admin", "author"):
        return jsonify({"error": "Insufficient permissions"}), 403
    data = request.get_json()
    if not data or not data.get("title") or not data.get("body"):
        return jsonify({"error": "Missing fields"}), 400
    slug = make_slug(data["title"])
    status = data.get("status", "draft")
    create_post(data["title"], slug, data["body"], user["id"], status)
    return jsonify({"message": "Post created", "slug": slug}), 201
