from flask import Blueprint, request, jsonify
from app.models.comment import get_comments_for_post, create_comment, delete_comment
from app.models.post import get_post_by_id
from app.auth.session import require_role

comments_bp = Blueprint("comments", __name__)


@comments_bp.route("/api/posts/<int:post_id>/comments")
def list_comments(post_id):
    comments = get_comments_for_post(post_id)
    return jsonify({"comments": [dict(c) for c in comments]})


@comments_bp.route("/api/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()
    if not data or not data.get("author_name") or not data.get("body"):
        return jsonify({"error": "Missing fields"}), 400
    create_comment(post_id, data["author_name"], data["body"])
    return jsonify({"message": "Comment added"}), 201


@comments_bp.route("/api/comments/<int:comment_id>", methods=["DELETE"])
def remove_comment(comment_id):
    user = require_role("admin")
    if not user:
        return jsonify({"error": "Unauthorized"}), 403
    delete_comment(comment_id)
    return jsonify({"message": "Comment deleted"})
