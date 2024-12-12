from candle import update_candle
from loguru import logger
from quixstreams import Application
from technical_indicators import compute_indicators


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    max_candles_in_state: int,
    candle_seconds: int,
):
    """
    1. ingests candles from the kafka topic
    2. processes candles and generates indicators
    3. pushes indicators to the kafka topic

    Args:
        kafka_broker_address (str): kafka broker address
        kafka_input_topic (str): topic to read candles from
        kafka_output_topic (str): topic to push indicators to
        kafka_consumer_group (str): kafka consumer group
        max_candles_in_state (int): number of candles to keep in state
        candle_seconds (int): size of the candles in seconds

    Returns:
        None
    """
    logger.info('starting ta service!')

    # initialize the quixstreams application
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    # Define a topic where the candles will be read
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
    )

    # Define a topic where the indicators will be pushed
    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer='json',
    )

    # Create a streaming dataframe for transforming
    sdf = app.dataframe(topic=input_topic)

    # we only keep the candles with the same windows size as the candle_seconds
    sdf = sdf[sdf['candle_seconds'] == candle_seconds]

    # update the list of candles in the state
    sdf = sdf.apply(update_candle, stateful=True)

    # compute the technical indicators from the candles in the state
    sdf = sdf.apply(compute_indicators, stateful=True)

    sdf = sdf.update(lambda value: logger.debug(f'final message: {value}'))

    # send the final message to the output topic
    sdf = sdf.to_topic(topic=output_topic)

    # Clear the state before running due to potential offset issues
    app.clear_state()

    app.run()


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        max_candles_in_state=config.max_candles_in_state,
        candle_seconds=config.candle_seconds,
    )
