import json
from typing import Optional

from loguru import logger
from quixstreams import Application

from src.feature_store_config import config
from src.hopsworks_api import data_to_feature_store


def kafka_to_feature_store(
    kafka_topic: str,
    kafka_broker_address: str,
    feature_group_name: str,
    feature_group_version: int,
    buffer_size: Optional[int],
    live_or_historical,
):
    """
    Reads OHLC data from Kafka topic and writes it to the Hopsworks feature store

    Args:
        kafka_topic (str): Kafka topic to read from
        kafka_broker_address (str): Kafka broker address
        feature_group_name (str): Name of the feature group to write to
        feature_group_version (int): Version of the feature group to write to
        buffer_size (intL optional): Number of messages to buffer before writing to the feature store
        live_or_historical (str): The type of data to write to the feature store.

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group='kafka_to_feature_store',
        auto_offset_reset='earliest',
    )

    # buffer to push ohlc data to feature store in batches
    buffer = []

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
                ohlc = json.loads(msg.value().decode('utf-8'))

                # TODO: temporary logging to see the data. To be removed in production.
                logger.info(f'Received OHLC data: {ohlc} | size: {len(buffer)}')

                buffer.append(ohlc)
                if buffer_size is not None and len(buffer) >= buffer_size:
                    # Write the OHLC data to the feature store in Hopsworks
                    data_to_feature_store(
                        feature_group_name=feature_group_name,
                        feature_group_version=feature_group_version,
                        data=buffer,
                        online_or_offline=live_or_historical,
                    )

                    # Reset the buffer
                    buffer = []

            consumer.store_offsets(message=msg)


if __name__ == '__main__':
    logger.debug(config.model_dump())
    # Catch KeyboardInterrupt to exit gracefully
    try:
        kafka_to_feature_store(
            kafka_topic=config.kafka_topic,
            kafka_broker_address=config.kafka_broker_address,
            feature_group_name=config.feature_group_name,
            feature_group_version=config.feature_group_version,
            buffer_size=config.buffer_size,
            live_or_historical=config.live_or_historical,
        )
    except KeyboardInterrupt:
        logger.info('Exiting kafka_to_feature_store...')
