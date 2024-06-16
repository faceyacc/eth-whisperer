from quixstreams import Application
from loguru import logger
from src.ohlc_config import config
from quixstreams import message_context
from datetime import timedelta


def trade_to_ohlc(
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_broker_addr: str,
    ohlc_window_seconds: int
) -> None:
    """
    Reads trades from Kafka input topic
    Aggregates them into OHLC candels using a given window in 'ohlc_windown_seconds'
    Saves ohlc data into another Kafka topic

    Args:
        kafka_input_topic (str): Kafka topic to read trade data from.
        kafka_output_topic (str): Kafka topic to write ohlc data to.
        kafka_broker_addr (str): Kafka broker address.
        ohlc_window_seconds (int): Window size in seconds for OHLC aggregation

    Return:
        None
    """

    # Handles low level communication with Kafka
    app = Application(
        broker_address=kafka_broker_addr,
        consumer_group="trade_to_ohlc",
        auto_offset_reset='earliest',

    )

    # Define input and output topics
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')
    input_topic = app.topic(name=kafka_input_topic, value_serializer='json')


    # Create StreamingDataFrame to apply transformations
    sdf = app.dataframe(input_topic)


    # Apply transformation to incoming data
    sdf = (
        sdf.tumbling_window(duration_ms=timedelta(seconds=ohlc_window_seconds))
        .reduce(reducer=update_ohlc_candle, initializer=init_ohlc_candle)

    )

    sdf = sdf.update(logger.info)

    sdf = sdf.to_topic(output_topic)

    # Run pipeline
    app.run(sdf)

if __name__ == '__main__':
    trade_to_ohlc(
        kafka_output_topic= config.kafka_output_topic,
        kafka_input_topic = config.kafka_input_topic,
        kafka_broker_addr= config.kafka_broker_addr,
        ohlc_window_seconds= config.ohlc_window_seconds,
    )
