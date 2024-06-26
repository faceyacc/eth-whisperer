import time
from typing import Dict, List

from loguru import logger
from quixstreams import Application

from src.kraken_api.kraken_rest import KrakenRestAPI
from src.kraken_api.websocket import KrakenWebsocketTradeAPI
from src.producer_config import config


def produce_trades(
    kafka_broker_address: str,
    kafka_topic_name: str,
    product_id: List[str],
    live_or_historical,
    last_n_days: int,
) -> None:
    """
    Reads trades from Kraken websocket API and saves them to Kafka topic.

    Args:
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_topic_name (str): The name of the Kafka topic.
        product_id (str): The id/ticker to get trade from Kraken API.
        live_or_historical (str): The type of data to get from Kraken API (live or historical).
        last_n_days (int): The number of days to get historical data.

    Returns:
        None
    """
    app = Application(broker_address=kafka_broker_address)

    # The topic to save trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    # Create kraken api instance.
    if live_or_historical == 'live':
        kraken_api = KrakenWebsocketTradeAPI(product_id=product_id)
    else:
        # get current timestamp in milliseconds
        to_timestamp = int(time.time() * 1000)  # to_timestamp
        from_timestamp = to_timestamp - (last_n_days * 24 * 60 * 60 * 1000)

        kraken_api = KrakenRestAPI(
            pairs=product_id, from_timestamp=from_timestamp, to_timestamp=to_timestamp
        )

    logger.info('Creating producer...')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            # check if we are done getting historical data
            if kraken_api is KrakenRestAPI and kraken_api.done():
                logger.info('Done getting historical data.')
                break

            trades: List[Dict] = kraken_api.get_trades()
            for trade in trades:
                message = topic.serialize(key=trade['product_id'], value=trade)

                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'trade => {trade}')


if __name__ == '__main__':
    produce_trades(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        product_id=config.product_id,
        # The type of data to get from Kraken API (live or historical)
        live_or_historical=config.live_or_historical,
        last_n_days=config.last_n_days,
    )
