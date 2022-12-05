import logging

import pandas as pd
from pydantic import BaseModel
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../../debug.log"),
        logging.StreamHandler()
    ]
)


class AmazonTrainService:
    file_location = "amazon_product/file/sample_product.csv"

    class Config:
        arbitrary_types_allowed = True

    def __init__(self):
        print('init')

    def hello(self):
        logging.info("hello")
        return "hello train"

    def train_model(self):
        logging.info("train")
        logging.info("self.file_location {} " + self.file_location)
        df = pd.read_csv(self.file_location)
        features = ['Product Name', 'Category', 'About Product', 'Product Specification', 'Technical Details']
        for feature in features:
            df[feature] = df[feature].fillna("")

        df['combined_features'] = df['Product Name'] + ' ' + df['About Product'] + ' ' + df['Category'] + ' ' + df[
            'Product Specification'] + ' ' + df['Technical Details']
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df.combined_features)
        A_sparse = sparse.csr_matrix(count_matrix)
        sparse.save_npz("amazon_product/file/amazon_model.npz", A_sparse)
