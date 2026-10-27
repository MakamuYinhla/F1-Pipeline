import logging
import pandas as pd
import requests

logger = logging.getLogger(__name__)


def extract_meta(_data):
    first_line = _data[0]
    meta_keys = list(first_line.keys())

    meta_line = ""
    for meta in meta_keys:
        meta_line += f"{meta},"

    meta_line = meta_line[:-1]

    return meta_line


def extract_data(_data):
    data_lines = ""
    
    for line in _data:
        values_list = list(line.values())
        lines = ""
        for value in values_list:
            lines += f"{value},"
    
        data_lines += f"{lines[:-1]}\n"

    return data_lines[:-1]


def extract(url_dict, data_folder):
    url_df = pd.array(url_dict)
    
    logger.info("URLs Loaded")
    
    for obj in url_df:
        try:    
            file_name = obj['type']
            logger.info(f"Starting extracting data for {file_name}")
            data_results = requests.get(obj['url'])
            _data = data_results.json()

            meta_data = extract_meta(_data)
            file_data = extract_data(_data)

            with open(f"{data_folder}/{file_name}.csv", "+w") as file:
                file.write(f"{meta_data}\n")
                file.write(file_data)

            logger.info(f"Finalizing file : {data_folder}\{file_name}.csv")
        except Exception:
            logger.error(Exception)

