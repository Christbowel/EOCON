from flask import Blueprint, request, jsonify
from app.models.post import (
    get_published_posts, get_post_by_slug, get_post_by_id,
    create_post, update_post, delete_post, count_published_posts
)
from app.models.comment import get_comments_for_post
from app.models.tag import get_tags_for_post
from app.auth.session import require_role
from app.lib.slugify import make_slug
from app.lib.pagination import paginate

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/api/posts")
def list_posts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    total = count_published_posts()
    offset = (page - 1) * per_page
    posts = get_published_posts(limit=per_page, offset=offset)
    return jsonify({
        "posts": [dict(p) for p in posts],
        "pagination": paginate(total, page, per_page),
    })


@posts_bp.route("/api/posts/<slug>")
def show_post(slug):
    post = get_post_by_slug(slug)
    if not post:
        return jsonify({"error": "Not found"}), 404
    comments = get_comments_for_post(post["id"])
    tags = get_tags_for_post(post["id"])
    result = dict(post)
    result["comments"] = [dict(c) for c in comments]
    result["tags"] = [dict(t) for t in tags]
    return jsonify(result)


@posts_bp.route("/api/posts", methods=["POST"])
def create():
    user = require_role("author")
    if not user:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json()
    if not data or not data.get("title") or not data.get("body"):
        return jsonify({"error": "Missing fields"}), 400
    slug = make_slug(data["title"])
    status = data.get("status", "draft")
    create_post(data["title"], slug, data["body"], user["id"], status)
    return jsonify({"message": "Post created", "slug": slug}), 201


@posts_bp.route("/api/posts/<int:post_id>", methods=["PUT"])
def edit(post_id):
    user = require_role("author")
    if not user:
        return jsonify({"error": "Unauthorized"}), 403
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Not found"}), 404
    if post["author_id"] != user["id"] and user["role"] != "admin":
        return jsonify({"error": "Forbidden"}), 403
    data = request.get_json()
    title = data.get("title", post["title"])
    body = data.get("body", post["body"])
    status = data.get("status", post["status"])
    update_post(post_id, title, body, status)
    return jsonify({"message": "Post updated"})


@posts_bp.route("/api/posts/<int:post_id>", methods=["DELETE"])
def remove(post_id):
    user = require_role("admin")
    if not user:
        return jsonify({"error": "Unauthorized"}), 403
    delete_post(post_id)
    return jsonify({"message": "Post deleted"})
