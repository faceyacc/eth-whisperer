import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(usecwd=True))

class Config(BaseSettings):
    product_id: str
    kafka_broker_address: str
    kafka_topic_name: str


config = Config() # pyright: ignore
