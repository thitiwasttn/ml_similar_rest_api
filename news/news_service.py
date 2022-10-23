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
    prefix="/news",
    responses={404: {'message': "Not found"}}
)


class NewsService(BaseModel):
    abc = ''
    df: pd.DataFrame = None
    A_sparse = []

    def __int__(self):
        self.reload()
        self.A_sparse = None

    class Config:
        arbitrary_types_allowed = True

    def get_csv(self):
        self.df = pd.read_csv('news/file/t1_thai_sum_v2.csv')

    def print_csv(self):
        self.reload_if_empty()

    def reload_if_empty(self):
        if self.df is None:
            self.reload()

    def reload(self):
        self.get_csv()
        self.A_sparse = sparse.load_npz("news/file/news_th.npz")

    def get_similar_product(self, ref_index):
        self.reload_if_empty()
        cosine_sim = cosine_similarity(self.A_sparse, self.A_sparse.getrow(ref_index))
        similar_products = list(enumerate(cosine_sim))
        sorted_similar_products = sorted(similar_products, key=lambda x: x[1], reverse=True)[1:][:8]
        return sorted_similar_products

    def get_index(self, product_id):
        ref_index = self.df[self.df['id'] == product_id].index[0]
        return ref_index


news_service = NewsService()
news_service.reload_if_empty()


def parse_csv(df):
    res = df.to_json()
    parsed = json.loads(res)
    return parsed


@router.get('/')
def base():
    return {
        "status": "ok"
    }


@router.get("/items/{item_id}")
def read_item(item_id: int):
    ref_index = news_service.get_index(item_id)
    print("ref_index ", ref_index)
    news = news_service.df.iloc[ref_index]
    return {
        "itemId": item_id,
        "index": int(ref_index),
        "obj": parse_csv(news)
    }


@router.get('/size')
def get_size():
    shape = news_service.df.shape
    return {
        "row": shape[0],
        "column": shape[1]
    }


@router.get("/similar/{item_id}")
def read_item(item_id: int):
    objs = []
    news = {}

    try:
        ref_index = int(news_service.get_index(item_id))
        similaies = news_service.get_similar_product(ref_index)
        # news = parse_csv(news_service.df.iloc[ref_index])
        for i, element in enumerate(similaies):
            similar_news = {}
            index = element[0]
            id = news_service.df['id'][index]
            # similar_news = parse_csv(df)
            similar_news['id'] = int(id)
            similar_news['score'] = element[1][0]
            objs.append(similar_news)
    except:
        print('error')

    return {
        "itemId": item_id,
        "item": news,
        "similar": objs
    }
