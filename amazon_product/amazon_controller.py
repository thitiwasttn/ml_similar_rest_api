import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import json

from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
import logging

from amazon_product.amazon_service import AmazonService

router = APIRouter(
    prefix="/amazon",
    tags=['Coffee'],
    responses={404: {'message': "Not found"}}
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../debug.log"),
        logging.StreamHandler()
    ]
)

amazon_service = AmazonService()
amazon_service.reload_if_empty()


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

