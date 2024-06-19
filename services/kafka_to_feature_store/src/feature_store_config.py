import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Config(BaseSettings):
    # ohlc_window_seconds: int = int(os.environ["OHLC_WINDOW_SECONDS"])

    kafka_topic: str = 'ohlc'
    kafka_broker_address: str = 'localhost:9092'
    hopsworks_project_name: str = 'eth_whisperer'
    hopsworks_api_key: str = os.environ['HOPSWORKS_KEY']
    feature_group_name: str = 'ohlc_feature_group'
    feature_group_version: int = 1


config = Config()
