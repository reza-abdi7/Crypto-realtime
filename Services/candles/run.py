from datetime import timedelta
from typing import Any, List, Optional, Tuple

from loguru import logger
from quixstreams import Application
from quixstreams.models import TimestampType


def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
    """
    Specifying a custom timestamp extractor to use the timestamp from the message payload
    instead of Kafka timestamp.
    """
    # timestamp_ms is a field added by the trades service
    return value['timestamp_ms']


def init_candle(trade: dict) -> dict:
    """
    Initialize the candle with the first trade

    Args:
        trade (dict): trade to initialize the candle with

    Returns:
        dict: initialized candle
    """
    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['volume'],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    """
    Update the candle with the new trade

    Args:
        candle (dict): candle to update
        trade (dict): trade to update the candle with

    Returns:
        dict: updated candle
    """
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['close'] = trade['price']
    candle['volume'] += trade['volume']
    return candle


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
):
    """
    1. ingests trades from the kafka topic
    2. processes trades and generates candles using tumbling window
    3. pushes candles to the kafka topic

    Args:
        kafka_broker_address (str): kafka broker address
        kafka_input_topic (str): topic to read trades from
        kafka_output_topic (str): topic to push candles to
        kafka_consumer_group (str): kafka consumer group
        candles_seconds (int): size of the candles in seconds

    Returns:
        None
    """

    logger.info('starting candles service!')

    # initialize the quixstreams application
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    # Define a topic where the trades will be read
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
        timestamp_extractor=custom_ts_extractor,
    )

    # Define a topic where the candles will be pushed
    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer='json',
    )

    # create a streaming dataframe from the input topic
    sdf = app.dataframe(topic=input_topic)

    # start defining the transformation, for our candles service is stateful transformation using windowed aggregation
    # quixstreams documentation https://quix.io/docs/quix-streams/windowing.html#updating-window-definitions

    # define tumbling window
    sdf = sdf.tumbling_window(timedelta(seconds=candle_seconds))

    # define aggregation
    sdf = sdf.reduce(reducer=update_candle, initializer=init_candle)

    # emit all intermediate candles to make the system more responsive
    sdf = sdf.current()

    # if you want to emit the final canndle only, use the followinhg
    # sdf = app.final()

    # Note, it can also be piped together like this in the examole in
    # https://quix.io/docs/quix-streams/windowing.html#updating-window-definitions

    # push the candles to the output topic
    sdf = sdf.to_topic(topic=output_topic)

    # start the application
    app.run()


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_seconds=config.candle_seconds,
    )
