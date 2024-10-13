import os
import sys
import pickle
import pandas as pd
from products_recommender.logger.log import logging
from products_recommender.config.configuration import AppConfiguration
from products_recommender.exception.exception_handler import AppException



class DataTransformation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config= app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e


    
    def get_data_transformer(self):
        try:
            df = pd.read_csv(self.data_transformation_config.clean_data_file_path)
            # Lets create a pivot table
            product_pivot = df.pivot_table(columns='user_id', index='product_name', values= 'rating')
            logging.info(f" Shape of product pivot table: {product_pivot.shape}")
            product_pivot.fillna(0, inplace=True)

            #saving pivot table data
            os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
            pickle.dump(product_pivot,open(os.path.join(self.data_transformation_config.transformed_data_dir,"transformed_data.pkl"),'wb'))
            logging.info(f"Saved pivot table data to {self.data_transformation_config.transformed_data_dir}")

            #keeping products name
            product_names = product_pivot.index

            #saving product_names objects for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(product_names,open(os.path.join(self.data_validation_config.serialized_objects_dir, "product_names.pkl"),'wb'))
            logging.info(f"Saved product_names serialization object to {self.data_validation_config.serialized_objects_dir}")

            #saving product_pivot objects for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(product_pivot,open(os.path.join(self.data_validation_config.serialized_objects_dir, "product_pivot.pkl"),'wb'))
            logging.info(f"Saved product_pivot serialization object to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            raise AppException(e, sys) from e

    

    def initiate_data_transformation(self):
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20} ")
            self.get_data_transformer()
            logging.info(f"{'='*20}Data Transformation log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e



