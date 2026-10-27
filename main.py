import sys
from pathlib import Path
from config.logger import logger_setup
from config.read_settings import read_settings_file
import logging
from extract.extractor import extract


log_folder = Path(__file__).parent.resolve() / "logs"
data_folder= Path(__file__).parent.resolve() / "data"


logger = logging.getLogger()

try:

    # Grab process type and check validity
    process_type = sys.argv[1]

    if process_type not in ("extract", "load", "transform"):
        raise Exception(f"Invalid process type passed in as argument: {process_type}")

    logger_setup(log_folder, process_type)
    
    if process_type == "extract":
        logger.info("Starting Extraction Process")
        settings = read_settings_file()
        extract(settings['extraction_url'], data_folder)

    elif process_type == "load":
        logger.info("Starting Loading Process")
        pass

    elif process_type == "transform":
        logger.info("Starting Transformation Process")
        pass
        
    
except IndexError:
    print("Missing Arguments on the run script")

except Exception as e:
    logger.error(e)


