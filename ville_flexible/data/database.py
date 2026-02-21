import json
import os


def get_assets():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_file_path = os.path.join(parent_dir, "data", "assets.json")
    with open(assets_file_path, "r") as assets_file:
        return json.load(assets_file)
