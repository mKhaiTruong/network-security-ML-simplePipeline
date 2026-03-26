import os, sys, pandas as pd, numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from src.network_security.exception.exception import NetworkSecurityException
from src.network_security.logging.logger import logger
from src.network_security.constants.training_pipeline import (
    TARGET_COLUMN, DATA_TRANSFORMATION_INPUT_PARAMS
)
from src.network_security.entity.artifact_config import (
    DataValidationArtifact,
    DataTransformationArtifact
)
from src.network_security.entity.entity_config import DataTransformationConfig
from src.network_security.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try: 
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_data_transformer_object(cls) -> Pipeline:
        logger.info(f"Entered data_transformer_object method of DataTransformation class...")
        
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_INPUT_PARAMS)
            logger.info(f"Initiated KNNImputerwith {DATA_TRANSFORMATION_INPUT_PARAMS}")
   
            return Pipeline([("imputer", imputer)])
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logger.info(f"Entered initiate_data_transformation method of DataTransformation class...")
        
        try:
            logger.info(f"Starting transformation")
            train_df = self.read_data(file_path=self.data_validation_artifact.valid_train_file_path)
            test_df  = self.read_data(file_path=self.data_validation_artifact.valid_test_file_path)
            
            input_feature_train_df  = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            input_feature_test_df   = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df  = test_df[TARGET_COLUMN]
            target_feature_test_df  = target_feature_test_df.replace(-1, 0)
            
            processor = self.get_data_transformer_object()
            preprocessor_obj = processor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature  = preprocessor_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr  = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            
            # Save numpy array data files
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr, )
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj, )
            
            # Prep artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)