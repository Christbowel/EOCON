from flask import Blueprint, jsonify
from app.models.tag import (
    get_all_tags, get_tag_by_slug, get_posts_by_tag,
    get_all_categories, get_category_by_slug, get_posts_by_category
)

tags_bp = Blueprint("tags", __name__)


@tags_bp.route("/api/tags")
def list_tags():
    tags = get_all_tags()
    return jsonify({"tags": [dict(t) for t in tags]})


@tags_bp.route("/api/tags/<slug>")
def show_tag(slug):
    tag = get_tag_by_slug(slug)
    if not tag:
        return jsonify({"error": "Not found"}), 404
    posts = get_posts_by_tag(tag["id"])
    return jsonify({"tag": dict(tag), "posts": [dict(p) for p in posts]})


@tags_bp.route("/api/categories")
def list_categories():
    cats = get_all_categories()
    return jsonify({"categories": [dict(c) for c in cats]})


@tags_bp.route("/api/categories/<slug>")
def show_category(slug):
    cat = get_category_by_slug(slug)
    if not cat:
        return jsonify({"error": "Not found"}), 404
    posts = get_posts_by_category(cat["id"])
    return jsonify({"category": dict(cat), "posts": [dict(p) for p in posts]})
