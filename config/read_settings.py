import json
from pathlib import Path
import logging

settings_file_path = Path(__file__).parent.parent / "settings.json"

logger = logging.getLogger()

def read_settings_file():
    global settings
    with open(settings_file_path) as file:
        settings  = json.load(file)

    logger.info("Settings file loaded")
    return settings
