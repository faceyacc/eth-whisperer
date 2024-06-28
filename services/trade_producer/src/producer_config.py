from typing import List

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(usecwd=True))


class Config(BaseSettings):
    kafka_broker_address: str = 'localhost:19092'  # default to local broker address
    kafka_topic_name: str
    product_id: List[str] = [
        'ETH/USD',
        'BTC/USD',
        'ETH/EUR',
        'BTC/EUR',
    ]

    # The type of data to get from Kraken API (live or historical)
    # live_or_historical: Literal['live', 'historical']
    live_or_historical: str = 'live'
    last_n_days: int = 3


config = Config()  # pyright: ignore
