import json

from loguru import logger
from quixstreams import Application

from src.feature_store_config import config
from src.hopsworks_api import data_to_feature_store


def kafka_to_feature_store(
    kafka_topic: str,
    kafka_broker_address: str,
    feature_group_name: str,
    feature_group_version: int,
):
    """
    Reads OHLC data from Kafka topic and writes it to the Hopsworks feature store

    Args:
        kafka_topic (str): Kafka topic to read from
        kafka_broker_address (str): Kafka broker address
        feature_group_name (str): Name of the feature group to write to
        feature_group_version (int): Version of the feature group to write to

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group='kafka_to_feature_store',
    )

    # Create a consumer to read from the Kafka topic
    with app.get_consumer() as consumer:
        consumer.subscribe(topics=[kafka_topic])

        while True:
            msg = consumer.poll(1)  # poll for messages every second
            if msg is None:
                continue
            elif msg.error():
                logger.error(f'Consumer error: {msg.error()}')
                continue
            else:
                ohlc = json.loads(msg.value())
                data_to_feature_store(
                    feature_group_name=feature_group_name,
                    feature_group_version=feature_group_version,
                    data=ohlc,
                )

            consumer.store_offsets(message=msg)


if __name__ == '__main__':
    kafka_to_feature_store(
        kafka_topic=config.kafka_topic,
        kafka_broker_address=config.kafka_broker_address,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
    )
