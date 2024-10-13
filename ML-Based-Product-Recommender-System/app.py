import os
import sys
import pickle
import streamlit as st
import numpy as np
from products_recommender.logger.log import logging
from products_recommender.config.configuration import AppConfiguration
from products_recommender.pipeline.training_pipeline import TrainingPipeline
from products_recommender.exception.exception_handler import AppException


class Recommendation:
    def __init__(self,app_config = AppConfiguration()):
        try:
            self.recommendation_config= app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e


    # def fetch_poster(self,suggestion):
    #     try:
    #         product_name = []
    #         ids_index = []
    #         poster_url = []
    #         product_pivot =  pickle.load(open(self.recommendation_config.product_pivot_serialized_objects,'rb'))
    #         final_rating =  pickle.load(open(self.recommendation_config.final_rating_serialized_objects,'rb'))

    #         for product_id in suggestion:
    #             product_name.append(product_pivot.index[product_id])

    #         for name in product_name[0]: 
    #             ids = np.where(final_rating['title'] == name)[0][0]
    #             ids_index.append(ids)

    #         for idx in ids_index:
    #             url = final_rating.iloc[idx]['image_url']
    #             poster_url.append(url)

    #         return poster_url
        
    #     except Exception as e:
    #         raise AppException(e, sys) from e
        
    def fetch_ratings(self,suggestion):
        try:
            product_name = []
            ids_index = []
            ratings = []
            product_pivot =  pickle.load(open(self.recommendation_config.product_pivot_serialized_objects,'rb'))
            final_rating =  pickle.load(open(self.recommendation_config.final_rating_serialized_objects,'rb'))

            for product_id in suggestion:
                product_name.append(product_pivot.index[product_id])

            for name in product_name[0]: 
                ids = np.where(final_rating['product_name'] == name)[0][0]
                ids_index.append(ids)

            for idx in ids_index:
                url = final_rating.iloc[idx]['num_of_rating']
                ratings.append(url)

            return ratings
        
        except Exception as e:
            raise AppException(e, sys) from e

    def recommend_product(self,product_name):
        try:
            products_list = []
            model = pickle.load(open(self.recommendation_config.trained_model_path,'rb'))
            product_pivot =  pickle.load(open(self.recommendation_config.product_pivot_serialized_objects,'rb'))
            product_id = np.where(product_pivot.index == product_name)[0][0]
            distance, suggestion = model.kneighbors(product_pivot.iloc[product_id,:].values.reshape(1,-1), n_neighbors=6 )

            # Kosh poster_url = self.fetch_poster(suggestion)
            ratings = self.fetch_ratings(suggestion)
            
            for i in range(len(suggestion)):
                    products = product_pivot.index[suggestion[i]]
                    for j in products:
                        products_list.append(j)
            # return products_list
            # Kosh return products_list , poster_url   
            return products_list , ratings   
        except Exception as e:
            raise AppException(e, sys) from e


    def train_engine(self):
        try:
            obj = TrainingPipeline()
            obj.start_training_pipeline()
            st.text("Training Completed!")
            logging.info(f"Recommended successfully!")
        except Exception as e:
            raise AppException(e, sys) from e

    
# Kosh    def recommendations_engine(self,selected_products):
        # try:
        #     # recommended_products,poster_url = self.recommend_product(selected_products)
        #     recommended_products = self.recommend_product(selected_products)
        #     col1, col2, col3, col4, col5 = st.columns(5)
        #     with col1:
        #         st.text(recommended_products[1])
        #         print("\r\n")
        #         # st.image(poster_url[1])
        #     with col2:
        #         st.text(recommended_products[2])
        #         # st.image(poster_url[2])

        #     with col3:
        #         st.text(recommended_products[3])
        #         # st.image(poster_url[3])
        #     with col4:
        #         st.text(recommended_products[4])
        #         # st.image(poster_url[4])
        #     with col5:
        #         st.text(recommended_products[5])
        #         # st.image(poster_url[5])
        # except Exception as e:
        #     raise AppException(e, sys) from e

    def recommendations_engine(self, selected_products):
        try:
            # Get the recommended products (Assuming it returns a list of products)
            recommended_products,userratings = self.recommend_product(selected_products)

            # Add a heading for the recommendations
            st.header("Top 5 Recommendations/Matches")

            # Add custom CSS for styling
            st.markdown("""
            <style>
            .product-recommendation {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
                border-bottom: 2px solid #f2f2f2;
                padding-bottom: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

            # Display the recommendations one below the other
            for i, product in enumerate(recommended_products[1:6], start=1):
                st.markdown(f"<div class='product-recommendation'>{i}. {product} - Rated by {userratings[i]} users</div>", unsafe_allow_html=True)

        except Exception as e:
            raise AppException(e, sys) from e



if __name__ == "__main__":
    st.header('ML Based products Recommender System')
    st.text("This is a collaborative filtering based recommendation system!")

    obj = Recommendation()

    #Training
    if st.button('Train Recommender System'):
        obj.train_engine()

    product_names = pickle.load(open(os.path.join('templates','product_names.pkl') ,'rb'))
    selected_products = st.selectbox(
        "Type or select a product from the dropdown",
        product_names)
    
    #recommendation
    if st.button('Show Recommendation'):
        obj.recommendations_engine(selected_products)
