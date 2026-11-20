import os
from flask import Blueprint, current_app, send_file, jsonify

files_bp = Blueprint("files", __name__)


@files_bp.route("/files/<path:name>")
def serve_file(name):
    upload_dir = current_app.config["UPLOAD_DIR"]
    filepath = os.path.join(upload_dir, name)
    if not os.path.isfile(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath)
