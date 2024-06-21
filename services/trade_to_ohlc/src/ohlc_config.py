import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(usecwd=True))

class Config(BaseSettings):
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_broker_addr: str
    ohlc_window_seconds: int = int(os.environ['OHLC_WINDOW_SECONDS'])


config = Config() # pyright: ignore
