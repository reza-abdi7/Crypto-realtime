from typing import Literal

from loguru import logger
from quixstreams import Application
from sink import HopsworksFeatureStoreSink


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    output_sink: HopsworksFeatureStoreSink,
    data_source: Literal['live', 'historical'],
):
    """
    2 things:
    1. reads messages from the kafka topic
    2. push the messages to the feature store

    Args:
        kafka_broker_address (str): the kafka broker address
        kafka_input_topic (str): the kafka input topic
        kafka_consumer_group (str): the kafka consumer group
        output_sink:  the output store sink
        data_source: the data source ('live', 'historical')
    """
    logger.info('staring service to-feature-store!')

    # initialize the quixstreams application
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='latest' if data_source == 'live' else 'earliest',
    )

    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
    )

    sdf = app.dataframe(input_topic)

    # Do some processing here ...
    # We need to extract the features we want to push to the feature store
    # TODO: Implement
    # Sink data to a CSV file
    # sdf.sink(csv_sink)
    sdf.sink(output_sink)

    app.run()
    # push messages to the feature store


if __name__ == '__main__':
    from config import config, hopsworks_credentials

    hopsworks_sink = HopsworksFeatureStoreSink(
        api_key=hopsworks_credentials.hopsworks_api_key,
        project_name=hopsworks_credentials.hopsworks_project_name,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
        feature_group_primary_key=config.feature_group_primary_key,
        feature_group_event_time=config.feature_group_event_time,
        feature_group_materialization_interval_minutes=config.feature_group_materialization_interval_minutes,
    )
    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        output_sink=hopsworks_sink,
        data_source=config.data_source,
    )
