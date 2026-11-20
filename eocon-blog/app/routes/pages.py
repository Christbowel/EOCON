from flask import Blueprint, render_template
from app.models.post import get_published_posts, get_post_by_id
from app.models.comment import get_comments_for_post
from app.models.tag import get_tags_for_post
from app.models.user import find_user_by_id

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    posts = get_published_posts(limit=20)
    enriched = []
    for p in posts:
        item = dict(p)
        item["tags"] = [dict(t) for t in get_tags_for_post(p["id"])]
        enriched.append(item)
    return render_template("index.html", posts=enriched)


@pages_bp.route("/post/<int:post_id>")
def show_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return "Not found", 404
    author = find_user_by_id(post["author_id"])
    post_data = dict(post)
    post_data["author_name"] = author["username"] if author else "unknown"
    comments = get_comments_for_post(post_id)
    tags = get_tags_for_post(post_id)
    return render_template("post.html", post=post_data, comments=comments, tags=tags)


@pages_bp.route("/preview")
def preview_page():
    return render_template("preview.html")
