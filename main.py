from src.network_security.components.data_ingestion import DataIngestion
from src.network_security.components.data_validation import DataValidation
from src.network_security.exception.exception import NetworkSecurityException
from src.network_security.logging.logger import logger
import os, sys

from src.network_security.entity.entity_config import DataIngestionConfig, DataValidationConfig
from src.network_security.entity.entity_config import TrainingPipelineConfig



if __name__ == "__main__":
    try:
        
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logger.info("Initiated data ingestion...")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logger.info("Data Ingestion Completed!")
        print(data_ingestion_artifact)
        
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logger.info("Initiated data validation...")
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info("Data Validation Completed!")
        print(data_validation_artifact)
        
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)