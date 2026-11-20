import os
import re
import subprocess

ALLOWED_NAME = re.compile(r"^[a-zA-Z0-9_\-]+\.[a-zA-Z]{3,4}$")


def generate_thumbnail(upload_dir, filename, size="128x128"):
    if not ALLOWED_NAME.match(filename):
        raise ValueError("Invalid filename")

    source = os.path.join(upload_dir, filename)
    if not os.path.isfile(source):
        raise FileNotFoundError("Source file not found")

    thumb_dir = os.path.join(upload_dir, "thumbs")
    os.makedirs(thumb_dir, exist_ok=True)

    dest = os.path.join(thumb_dir, "thumb_" + filename)

    subprocess.run(
        ["convert", source, "-resize", size, dest],
        check=True,
        capture_output=True
    )

    return dest
