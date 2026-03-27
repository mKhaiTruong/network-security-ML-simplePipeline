import os, sys

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
)

from src.network_security.logging.logger import logger
from src.network_security.exception.exception import NetworkSecurityException

from src.network_security.entity.artifact_config import DataTransformationArtifact, ModelTrainerArtifact
from src.network_security.entity.entity_config import ModelTrainerConfig

from src.network_security.utils.main_utils.utils import save_object, load_object
from src.network_security.utils.main_utils.utils import load_numpy_array_data
from src.network_security.utils.main_utils.utils import evaluate_models
from src.network_security.utils.ml_utils.metric.classification_metric import get_classification_score
from src.network_security.utils.ml_utils.model.estimator import NetworkModel

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                data_transformation_artifact: DataTransformationArtifact):
        try: 
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def train_model(self, X_train, y_train, x_test, y_test):
        
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier()
        }
        
        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
            },
            "Random Forest": {
                # 'criterion': ['gini', 'entropy', 'log_loss'],
                # 'max_features': ['sqrt', 'log2', None],
                'n_estimators': [8, 16, 32, 64, 128, 256],
            },
            "Gradient Boosting": {
                'learning_rate': [0.1, 0.01, 0.05, 0.001],
                'subsample': [0.6, 0.7, 0.075, 0.8, 0.85, 0.9],  
                'n_estimators':  [8, 16, 32, 64, 128, 256],
            },
            "Logistic Regression": {},
            "AdaBoost": {
                'learning_rate': [0.1, 0.01, 0.05, 0.001],
                'n_estimators':  [8, 16, 32, 64, 128, 256],
            },
        }
        
        model_report: dict = evaluate_models(
            X_train=X_train, y_train=y_train, x_test=x_test, y_test=y_test,
            models=models, param=params
        )
        
        best_model_score = max(sorted(model_report.values()))
        best_model_name  = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]
        
        y_train_pred = best_model.predict(X_train)
        classification_train_metrics = get_classification_score(y_true=y_train, y_pred=y_train_pred)
        
        # Track the MLFlow
        y_test_pred = best_model.predict(x_test)
        classification_test_metrics  = get_classification_score(y_true=y_test, y_pred=y_test_pred)
    
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)
        
        Network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=Network_model)
        
        # Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path = self.model_trainer_config.trained_model_file_path,
            train_metric_artifact = classification_train_metrics,
            test_metric_artifact = classification_test_metrics
        )
        logger.info(f"Model trainer artifact: {model_trainer_artifact} created!!")
        return model_trainer_artifact
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try: 
            logger.info(f"Entered initiate_model_trainer method of ModelTrainer class...")
            
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            transformed_test_file_path  = self.data_transformation_artifact.transformed_test_file_path
            
            train_arr = load_numpy_array_data(file_path=transformed_train_file_path)
            test_arr  = load_numpy_array_data(file_path=transformed_test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )
            
            return self.train_model(x_train, y_train, x_test, y_test)
        except Exception as e:
            raise NetworkSecurityException(e, sys)