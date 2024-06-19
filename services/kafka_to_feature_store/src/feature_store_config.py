import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Config(BaseSettings):
    # ohlc_window_seconds: int = int(os.environ["OHLC_WINDOW_SECONDS"])

    kafka_topic: str = os.environ['KAFKA_TOPIC']
    local_kafka_broker_addr: str = os.environ['LOCAL_KAFKA_BROKER_ADDR']
    hopsworks_project_name: str = os.environ['HOPSWORKS_PROJECT_NAME']
    hopsworks_api_key: str = os.environ['HOPSWORKS_KEY']
    feature_group_name: str = os.environ['FEATURE_GROUP_NAME']
    feature_group_version: int = int(os.environ['FEATURE_GROUP_VERSION'])


config = Config()
