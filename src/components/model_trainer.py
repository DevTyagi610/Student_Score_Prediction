import os
import sys
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object , evaluate_model

from catboost import CatBoostRegressor

from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from sklearn.metrics import r2_score

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts" , "model.pkl")

class ModelTrainer:
    def __init__(self) :
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try :
            logging.info("Spiltting Training and Testing data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1], # all rows (given by 1st ':') and cols of array except last col
                train_array[:, -1],  # only th last col 
                test_array[:, :-1],
                test_array[:,-1]
            )

            models = {
                "Random Forest" : RandomForestRegressor(),
                "Linear Regression" : LinearRegression(),
                "Decision Trees" : DecisionTreeRegressor(),
                "K Neighbors Classifier" : KNeighborsRegressor(),
                "Adaboost Regressor" : AdaBoostRegressor(),
                "Gradient Boosting" : GradientBoostingRegressor(),
                "CatBoosting Classifier" : CatBoostRegressor(),
                "XGBoost Classifier" : XGBRegressor()
            }

            model_report:dict = evaluate_model(X_train =  X_train, y_train = y_train, X_test = X_test,
                                                y_test = y_test, models = models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score < 0.6 :
                raise CustomException("No Best Model Found")
            
            logging.info("Best model found for training & testing data")

            save_object(file_path=self.model_trainer_config.trained_model_file_path,
                        obj = best_model)

            predicted = best_model.predict(X_test)
            r2 = r2_score(y_test, predicted)

            return r2
            
        except Exception as e:
            raise CustomException(e, sys)
        

