import json
import os

def parse_json(json_file_path):
    """parse a json file and return a dictionary"""
    # windows
    if os.name == "nt":
        print("running on Windows")
        json_file_path = json_file_path.replace("/", "\\")
        abs_path = os.path.abspath(json_file_path)
        parent_dir = os.path.dirname(abs_path)
        # append "detective" to the parent directory
        parent_dir = os.path.join(parent_dir, "detective")
        path = os.path.join(parent_dir, json_file_path)
    with open(path, "r") as file:
        return json.load(file)