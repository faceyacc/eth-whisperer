from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(usecwd=True))


class Config(BaseSettings):
    kafka_broker_address: str = 'localhost:19092'  # default to local broker address
    kafka_input_topic: str
    kafka_output_topic: str
    ohlc_window_seconds: int


config = Config()  # pyright: ignore
