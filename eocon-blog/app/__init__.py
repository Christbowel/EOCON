import os
from flask import Flask
from app.db import init_db, get_db
from app.seed import seed_database
from app.lib.config import load_config


def create_app():
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app = Flask(__name__)

    config = load_config()
    app.secret_key = config.get("secret_key", "fallback-secret")
    app.config["UPLOAD_DIR"] = os.path.join(base_dir, config.get("upload_dir", "uploads"))
    app.config["SITE"] = config
    app.config["DATABASE"] = os.path.join(base_dir, "eocon.db")

    init_db(app)

    with app.app_context():
        db = get_db()
        seed_database(db)

    from app.routes.pages import pages_bp
    from app.auth.routes import auth_bp
    from app.routes.posts import posts_bp
    from app.routes.comments import comments_bp
    from app.routes.tags import tags_bp
    from app.routes.search import search_bp
    from app.routes.preview import preview_bp
    from app.routes.files import files_bp
    from app.routes.feeds import feeds_bp
    from app.routes.api import api_bp
    from app.admin.routes import admin_bp
    from app.admin.console import console_bp
    from app.admin.settings import settings_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(preview_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(feeds_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(console_bp)
    app.register_blueprint(settings_bp)

    return app
