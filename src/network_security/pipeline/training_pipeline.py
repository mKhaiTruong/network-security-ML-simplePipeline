import os, sys

from src.network_security.exception.exception import NetworkSecurityException
from src.network_security.logging.logger import logger
from src.network_security.utils.main_utils.utils import read_yaml_file

from src.network_security.components.data_ingestion import DataIngestion
from src.network_security.components.data_validation import DataValidation
from src.network_security.components.data_transformation import DataTransformation
from src.network_security.components.model_trainer import ModelTrainer

from src.network_security.entity.entity_config import (
    TrainingPipelineConfig,
    DataIngestionConfig, 
    DataValidationConfig, 
    DataTransformationConfig,
    ModelTrainerConfig,
)
from src.network_security.entity.artifact_config import (
    DataIngestionArtifact, 
    DataValidationArtifact, 
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try: 
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            logger.info(f"Start data ingestion...")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info(f"Completed data ingestion!")
            
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try: 
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            logger.info(f"Start data validation...")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, 
                                            data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logger.info(f"Completed data validation!")
            
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try: 
            self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            logger.info(f"Start data transformation...")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, 
                                                     data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logger.info(f"Completed data transformation!")
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try: 
            self.model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            logger.info(f"Start model trainer...")
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config, 
                                         data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logger.info(f"Completed model trainer!")
            
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def run_pipeline(self):
        try: 
            data_ingestion_artifact  = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact   = self.start_model_trainer(data_transformation_artifact)
            
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)