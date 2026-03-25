import os, sys, yaml, numpy as np, pickle
from src.network_security.exception.exception import NetworkSecurityException
from src.network_security.logging.logger import logger

def read_yaml_file(file_path: str) -> dict:
    try: 
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try: 
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file_obj:
            yaml.dump(content, file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)