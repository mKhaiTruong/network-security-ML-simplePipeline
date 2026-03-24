import os, json, sys, pymongo, pandas as pd, numpy as np

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

from src.network_security.exception.exception import NetworkSecurityException
from src.network_security.logging.logger import logger

class NetworkDataExtract():
    def __init__(self):
        try: pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def csv_to_json_convertor(self, file_path):
        try: 
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = data.to_dict(orient="records")
            return records
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            
            self.collection.insert_many(self.records)
            return len(self.records)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_data\phisingData.csv"
    DATABASE = "MKHUE"
    COLLECTION = "NetworkData"
    
    net_obj = NetworkDataExtract()
    records = net_obj.csv_to_json_convertor(file_path=FILE_PATH)
    no_cols = net_obj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    print(no_cols)