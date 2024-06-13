from typing import Dict, List

from loguru import logger
from quixstreams import Application

from src.kraken_api import KrakenWebsocketTradeAPI
from src import config


def produce_trades(
    kafka_broker_address: str, kafka_topic_name: str, product_id: str
) -> None:
    """
    Reads trades from Kraken websocket API and saves them to Kafka topic.

    Args:
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_topic_name (str): The name of the Kafka topic.
        product_id (str): The id/ticker to get trade from Kraken API.

    Returns:
        None
    """
    app = Application(broker_address=kafka_broker_address)

    # The topic to save trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    # Create kraken api instance.
    kraken_api = KrakenWebsocketTradeAPI(product_id=config.product_id)

    logger.info('Creating producer...')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            trades: List[Dict] = kraken_api.get_trades()
            for trade in trades:
                message = topic.serialize(key=trade['product_id'], value=trade)

                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'trade => {trade}')

            from time import sleep

            sleep(1)


if __name__ == '__main__':
    produce_trades(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        product_id=config.product_id,
    )
