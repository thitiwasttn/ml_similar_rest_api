import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import json

from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/amazon",
    tags=['Coffee'],
    responses={404: {'message': "Not found"}}
)


class AmazonService(BaseModel):
    abc = ''
    df: pd.DataFrame = None
    A_sparse = []

    def __int__(self):
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


amazon_service = AmazonService()
amazon_service.reload()


@router.get('/size')
def get_size():
    shape = amazon_service.df.shape
    return {
        "row": shape[0],
        "column": shape[1]
    }


@router.get("/items/{item_id}")
def read_item(item_id: str):
    ref_index = amazon_service.get_index(item_id)
    product = amazon_service.df.iloc[ref_index]
    return {
        "itemId": item_id,
        "index": int(ref_index),
        "obj": parse_csv(product)
    }


@router.get("/reload")
def read_item():
    amazon_service.reload()
    return {
        "status": "ok"
    }


@router.get("/similar/{item_id}")
def read_item(item_id: str):
    objs = []
    ref_index = 0
    product = {}
    try:
        ref_index = amazon_service.get_index(item_id)
        product = amazon_service.df.iloc[ref_index]
        product = parse_csv(product)
        similaies = amazon_service.get_similar_product(ref_index)

        for i, element in enumerate(similaies):
            similar_product_id = element[0]
            df = amazon_service.df.iloc[similar_product_id]
            similar_product = parse_csv(df)
            similar_product['score'] = element[1][0]
            objs.append(similar_product)
    except:
        print('error')

    return {
        "itemId": item_id,
        "index": int(ref_index),
        "obj": product,
        "similar": objs
    }


def parse_csv(df):
    res = df.to_json()
    parsed = json.loads(res)
    return parsed
