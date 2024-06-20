import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Config(BaseSettings):
    kafka_topic: str = 'ohlc'
    kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
    hopsworks_project_name: str = os.environ['HOPSWORKS_PROJECT_NAME']
    hopsworks_api_key: str = os.environ['HOPSWORKS_API_KEY']
    feature_group_name: str = os.environ['FEATURE_GROUP_NAME']
    feature_group_version: int = int(os.environ['FEATURE_GROUP_VERSION'])


config = Config()
