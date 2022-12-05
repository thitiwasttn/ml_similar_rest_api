import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from pydantic import BaseModel

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


class AmazonService():
    abc = ''
    df: pd.DataFrame = None
    A_sparse = []

    def __int__(self):
        logging.info('init')
        self.reload()
        self.A_sparse = None

    class Config:
        arbitrary_types_allowed = True

    def hello(self):
        print('hello')
        return self.abc

    def get_csv(self):
        self.df = pd.read_csv('amazon_product/file/sample_product.csv')

    def print_csv(self):
        self.reload_if_empty()

    def reload_if_empty(self):
        if self.df is None:
            self.reload()

    def reload(self):
        logging.info('reload')
        self.get_csv()
        self.A_sparse = sparse.load_npz("amazon_product/file/amazon_model.npz")

    def get_similar_product(self, ref_index):
        self.reload_if_empty()
        cosine_sim = cosine_similarity(self.A_sparse, self.A_sparse.getrow(ref_index))
        similar_products = list(enumerate(cosine_sim))
        sorted_similar_products = sorted(similar_products, key=lambda x: x[1], reverse=True)[1:][:8]
        return sorted_similar_products

    def get_index(self, product_id):
        ref_index = self.df[self.df['Uniq Id'].str.contains(product_id, case=False)].index[0]
        return ref_index
