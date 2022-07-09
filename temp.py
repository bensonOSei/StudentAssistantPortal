"""
Author : Michael Kofi Armah
Description: Automatically files in missing parametes in gsheets_keys.json for GOOGLE SHEETS functionality
"""

import os
from dotenv import load_dotenv
import json

load_dotenv(".env")
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")

PRIVATE_KEY_ID = os.environ.get("PRIVATE_KEY_ID")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
CLIENT_EMAIL = os.environ.get("CLIENT_EMAIL")
CLIENT_ID = os.environ.get("CLIENT_ID")
PROJECT_ID = os.environ.get("PROJECT_ID")


def load_json():
    with open("./google_sheets_plugin/gsheets_keys.json", "r") as jfile:
        data = json.load(jfile)

    data.update({
        "project_id": PROJECT_ID,
        "private_key_id": PRIVATE_KEY_ID,
        "private_key": PRIVATE_KEY,
        "client_email": CLIENT_EMAIL,
        "client_id": CLIENT_ID
    })

    with open("./google_sheets_plugin/gsheets_keys.json", "w") as file:
        json.dump(data, file, indent=4)


data = load_json()
