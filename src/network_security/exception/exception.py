import sys
from network_security.logging.logger import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        _, _, self.exc_tb  = error_details.exc_info()
        
        self.lineno = self.exc_tb.tb_lineno
        self.file_name = self.exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return f"Error occurred in python script name [{self.error_message}]  at line number [{self.file_name}], error message: [{self.lineno}]"
    
if __name__ == "__main__":
    try:
        logger.info("ENTER TRY BLOCK")
        a = 1/0
        print(f'this will not be printed {a}')
    except Exception as e:
        raise NetworkSecurityException(e, sys)