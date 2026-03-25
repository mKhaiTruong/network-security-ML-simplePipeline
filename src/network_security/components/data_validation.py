import os, sys, pandas as pd
from scipy.stats import ks_2samp

from src.network_security.exception.exception import NetworkSecurityException
from src.network_security.logging.logger import logger
from src.network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file
from src.network_security.entity.artifact_config import DataIngestionArtifact, DataValidationArtifact
from src.network_security.entity.entity_config import DataValidationConfig
from src.network_security.constants.training_pipeline import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self, 
                 data_ingestion_artifact: DataIngestionArtifact, 
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config  = data_validation_config
            
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try: return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        try: 
            n_cols = len(self._schema_config)
            logger.info(f"Required number of columns: {n_cols}")
            logger.info(f"Data frame has columns: {len(df.columns)}")
            
            return (len(df.columns) == n_cols)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_data_drift(self, base_df, curr_df, threshold=0.05) -> bool:
        try: 
            status, report = True, {}
            
            for col in base_df.columns:
                is_same_dict = ks_2samp(base_df[col], curr_df[col])
                p_val = is_same_dict.pvalue
                
                if p_val > threshold:
                    is_found = False
                else:
                    is_found = True
                    status = False
                
                report.update({col: {
                    "p_value": float(p_val), 
                    "drift_status": is_found
                }})

            drift_report_file = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file), exist_ok=True)
            write_yaml_file(file_path=drift_report_file, content=report)
            
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try: 
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path  = self.data_ingestion_artifact.test_file_path
            
            train_df = DataValidation.read_data(train_file_path)
            test_df  = DataValidation.read_data(test_file_path)
            
            # Validate number of columns
            status = self.validate_number_of_columns(train_df)
            if not status: err_msg = f"Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(test_df)
            if not status: err_msg = f"Test dataframe does not contain all columns.\n"
            
            # Check data drift
            status = self.detect_data_drift(base_df=train_df, curr_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)