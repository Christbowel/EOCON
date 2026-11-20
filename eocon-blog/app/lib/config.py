import os
import yaml

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config.yml"
)


def load_config():
    if not os.path.isfile(CONFIG_PATH):
        return default_config()

    with open(CONFIG_PATH, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    if not isinstance(data, dict):
        return default_config()

    return data


def default_config():
    return {
        "site_name": "EOCON Blog",
        "tagline": "EyesOpen Conference 2026",
        "per_page": 10,
        "upload_dir": "uploads",
        "secret_key": "fallback-secret",
    }


def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
