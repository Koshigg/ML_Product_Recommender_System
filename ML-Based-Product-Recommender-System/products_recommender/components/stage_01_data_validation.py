import os
import sys
import ast 
import pandas as pd
import pickle
from products_recommender.logger.log import logging
from products_recommender.config.configuration import AppConfiguration
from products_recommender.exception.exception_handler import AppException



class DataValidation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_validation_config= app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e


    
    def preprocess_data(self):
        try:
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=",", on_bad_lines='skip', encoding='latin-1')
            products = pd.read_csv(self.data_validation_config.products_csv_file, sep=",", on_bad_lines='skip', encoding='latin-1')
            
            logging.info(f" Shape of user-product-ratings data file: {ratings.shape}")
            logging.info(f" Shape of products data file: {products.shape}")

            #Here Image URL columns is important for the poster. So, we will keep it
            products = products[['product_id','product_name', 'category', 'brand', 'price','product_rating']]
            # Lets remane some wierd columns name in products
            # Kosh products.rename(columns={"Book-Title":'title',
            #                     'Book-Author':'author',
            #                     "Year-Of-Publication":'year',
            #                     "Publisher":"publisher",
            #                     "Image-URL-L":"image_url"},inplace=True)

            
            # Lets remane some wierd columns name in ratings
            # Kosh ratings.rename(columns={"User-ID":'user_id',
            #                     'Book-Rating':'rating'},inplace=True)

            # Lets store users who had at least rated more than 200 products
            x = ratings['user_id'].value_counts() > 5
            y = x[x].index
            ratings = ratings[ratings['user_id'].isin(y)]

            # Now join ratings with products
            ratings_with_products = ratings.merge(products, on='product_id')
            # print(ratings_with_products.head())
            number_rating = ratings_with_products.groupby('product_name')['rating'].count().reset_index()
            number_rating.rename(columns={'rating':'num_of_rating'},inplace=True)
            final_rating = ratings_with_products.merge(number_rating, on='product_name')

            # Lets take those products which got at least 50 rating of user
            final_rating = final_rating[final_rating['num_of_rating'] >= 50]

            # Kosh added
            final_rating = final_rating.groupby('product_name', group_keys=False).apply(lambda x: x.sort_values('num_of_rating', ascending=False))

            # lets drop the duplicates
            final_rating.drop_duplicates(['user_id','product_name'],inplace=True)
            logging.info(f" Shape of the final clean dataset: {final_rating.shape}")
                        
            # Saving the cleaned data for transformation
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            final_rating.to_csv(os.path.join(self.data_validation_config.clean_data_dir,'clean_data.csv'), index = False)
            logging.info(f"Saved cleaned data to {self.data_validation_config.clean_data_dir}")


            #saving final_rating objects for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(final_rating,open(os.path.join(self.data_validation_config.serialized_objects_dir, "final_rating.pkl"),'wb'))
            logging.info(f"Saved final_rating serialization object to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            raise AppException(e, sys) from e

    
    def initiate_data_validation(self):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
            self.preprocess_data()
            logging.info(f"{'='*20}Data Validation log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e



    