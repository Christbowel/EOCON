from flask import Blueprint, request, jsonify
from app.models.post import search_posts

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/search")
def search():
    q = request.args.get("q", "")
    if not q or len(q) < 2:
        return jsonify({"error": "Query too short"}), 400
    results = search_posts(q)
    return jsonify({"query": q, "results": [dict(r) for r in results]})
