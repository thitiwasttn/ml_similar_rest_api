from typing import Union

from fastapi import FastAPI, Depends

from amazon_product import amazon_controller
from news import news_service
from amazon_product import amazon_train_controller

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "https://localhost.com",
    "http://localhost",
    "http://localhost:3000",
    "http://61.19.242.56",
    "http://61.19.242.56:7997",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def config_router():
    app.include_router(amazon_controller.router)
    app.include_router(news_service.router)
    app.include_router(amazon_train_controller.router)

config_router()
