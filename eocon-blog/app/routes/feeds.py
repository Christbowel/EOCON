from flask import Blueprint, Response
from app.models.post import get_published_posts

feeds_bp = Blueprint("feeds", __name__)


@feeds_bp.route("/feed/rss")
def rss_feed():
    posts = get_published_posts(limit=20)
    items = ""
    for p in posts:
        items += "<item>"
        items += "<title>{}</title>".format(p["title"])
        items += "<link>/api/posts/{}</link>".format(p["slug"])
        items += "<description>{}</description>".format(p["body"][:200])
        items += "<pubDate>{}</pubDate>".format(p["created_at"])
        items += "</item>\n"

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        "<channel>\n"
        "<title>EOCON Blog</title>\n"
        "<link>/</link>\n"
        "<description>EyesOpen Conference 2026</description>\n"
        "{}"
        "</channel>\n"
        "</rss>"
    ).format(items)

    return Response(xml, mimetype="application/rss+xml")


@feeds_bp.route("/feed/atom")
def atom_feed():
    posts = get_published_posts(limit=20)
    entries = ""
    for p in posts:
        entries += "<entry>"
        entries += "<title>{}</title>".format(p["title"])
        entries += "<id>{}</id>".format(p["slug"])
        entries += "<updated>{}</updated>".format(p["created_at"])
        entries += "<summary>{}</summary>".format(p["body"][:200])
        entries += "</entry>\n"

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        "<title>EOCON Blog</title>\n"
        "<id>eocon-blog</id>\n"
        "{}"
        "</feed>"
    ).format(entries)

    return Response(xml, mimetype="application/atom+xml")
