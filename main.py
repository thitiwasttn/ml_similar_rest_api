from typing import Union

from fastapi import FastAPI, Depends

from amazon_product import amazon_service
from news import news_service



app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def config_router():
    app.include_router(amazon_service.router)
    app.include_router(news_service.router)

config_router()
