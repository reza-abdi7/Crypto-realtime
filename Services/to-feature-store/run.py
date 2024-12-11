from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    feature_group_name: str,
    feature_group_version: int,
):
    """
    2 things:
    1. reads messages from the kafka topic
    2. push the messages to the feature store

    Args:
        kafka_broker_address (str): _description_
        kafka_input_topic (str): _description_
        kafka_consumer_group (str): _description_
        feature_group_name (str): _description_
        feature_group_version (int): _description_
    """
    logger.info('staring service to-feature-store!')

    # initialize the quixstreams application
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )

    # input_topic = app.topic(
    #     name=kafka_input_topic,
    #     value_deserializer='json',
    # )

    # Do some processing here ...
    # We need to extract the features we want to push to the feature store
    # TODO: Implement
    # Sink data to a CSV file
    # sdf.sink(csv_sink)

    app.run()
    # push messages to the feature store


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
    )
