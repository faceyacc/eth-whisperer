import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Config(BaseSettings):
    kafka_input_topic: str = "trade"
    kafka_output_topic: str = "ohlc"
    kafka_broker_addr: str = os.environ["KAFKA_BROKER_ADDRESS"]
    ohlc_window_seconds: int = int(os.environ["OHLC_WINDOW_SECONDS"])


config = Config()
