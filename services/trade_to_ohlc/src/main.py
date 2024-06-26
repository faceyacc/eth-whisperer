from datetime import timedelta
from loguru import logger
from quixstreams import Application
from src.ohlc_config import config
# import typing for Any, Optional, List, Tuple, TimestampType
from typing import Any, Optional, List, Tuple

def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type
) -> int:
    """
    Specifying a custom timestamp extractor to use the timestamp from the message payload
    instead of Kafka timestamp.
    """
    return value["timestamp"]


def init_ohlc_candle(value: dict) -> dict:
    """
    Initalize the OHLC candle with first trade
    """
    return {
        'open': value['price'],
        'high': value['price'],
        'low': value['price'],
        'close': value['price'],
        'product_id': value['product_id'],
    }


def update_ohlc_candle(ohlc_candle: dict, trade: dict) -> dict:
    """
    Update OHLC candle with new trade and return it

    Args:
        ohlc_candle (dict): The current OHLC candle.
        trade (dict): The incoming trade.
    Returns:
        dict: The updated candle.
    """
    return {
        'open': ohlc_candle['open'],
        'high': max(ohlc_candle['high'], trade['price']),
        'low': min(ohlc_candle['low'], trade['price']),
        'close': trade['price'],
        'product_id': trade['product_id'],
    }


def trade_to_ohlc(
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_broker_addr: str,
    kafka_consumer_group: str,
    ohlc_window_seconds: int,
) -> None:
    """
    Reads trades from Kafka input topic
    Aggregates them into OHLC candels using a given window in 'ohlc_windown_seconds'
    Saves ohlc data into another Kafka topic

    Args:
        kafka_input_topic (str): Kafka topic to read trade data from.
        kafka_output_topic (str): Kafka topic to write ohlc data to.
        kafka_broker_addr (str): Kafka broker address.
        kafka_consumer_group (str): Kafka consumer group.
        ohlc_window_seconds (int): Window size in seconds for OHLC aggregation

    Return:
        None
    """

    # Handles low level communication with Kafka
    app = Application(
        broker_address=kafka_broker_addr,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='earliest',
    )

    # Define input and output topics
    input_topic = app.topic(
        name=kafka_input_topic,
        value_serializer='json',
        # timestamp_extractor=custom_ts_extractor # pyright: ignore
    )
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # Create StreamingDataFrame to apply transformations
    sdf = app.dataframe(input_topic)

    # Apply transformation to incoming data
    # sdf = (
    #     sdf.tumbling_window(duration_ms=timedelta(seconds=ohlc_window_seconds))
    #     .reduce(reducer=update_ohlc_candle, initializer=init_ohlc_candle)
    #     .final()
    # )
    sdf = sdf.tumbling_window(duration_ms=timedelta(seconds=ohlc_window_seconds))
    sdf = sdf.reduce(reducer=update_ohlc_candle, initializer=init_ohlc_candle).final()

    # Unpack keys to get values
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['product_id'] = sdf['value']['product_id']
    sdf['timestamp'] = sdf['end']

    # # Extract crucial keys to give to Redpanda
    sdf = sdf[['timestamp', 'open', 'high', 'low', 'close', 'product_id']]

    sdf = sdf.update(logger.info)

    # Write data to output topic
    sdf = sdf.to_topic(output_topic)

    # breakpoint()
    # Run pipeline
    app.run(sdf)


if __name__ == '__main__':
    trade_to_ohlc(
        kafka_output_topic=config.kafka_output_topic,
        kafka_input_topic=config.kafka_input_topic,
        kafka_broker_addr=config.kafka_broker_address,
        kafka_consumer_group=config.kafka_consumer_group,
        ohlc_window_seconds=config.ohlc_window_seconds,
    )
