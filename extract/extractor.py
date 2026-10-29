import logging
import pandas as pd
import requests

logger = logging.getLogger(__name__)


def extract(url_dict, data_folder):
    url_df = pd.array(url_dict)
    
    logger.info("URLs Loaded")
    
    for obj in url_df:
        try:    
            file_name = obj['type']
            logger.info(f"Starting extracting data for {file_name}")
            data_results = requests.get(obj['url'])
            _data = data_results.json()

            out_path = f"{data_folder}/{file_name}.csv"
            pd.DataFrame(_data).to_csv(out_path, index=False)

            logger.info(f"Finalizing file : {out_path}")
        except Exception as e:
            logger.error(e)
            print(e)

