import logging

from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../../debug.log"),
        logging.StreamHandler()
    ]
)


class AmazonTrainService(BaseModel):

    def __init__(self):
        print('init')

    def hello(self):
        logging.info("hello")
        return "hello train"
