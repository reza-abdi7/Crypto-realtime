from loguru import logger
from news_data_source import NewsDataSource
from news_downloader import NewsDownloader
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    news_source: NewsDataSource,
):
    """
    Gets news from Cryptopanic and pushes it to a Kafka topic.

    Args:
        kafka_broker_address: The address of the Kafka broker.
        kafka_topic: The topic to push the news to.
        news_source: The news source to get the news from.
    Returns:
        None
    """
    logger.info("Hello from news!")

    app = Application(broker_address=kafka_broker_address)

    # Topic where we will push the news to
    output_topic = app.topic(name=kafka_topic, value_serializer="json")

    # Create the streaming dataframe
    sdf = app.dataframe(source=news_source)

    # Send the final messages to the output topic
    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == "__main__":
    from config import config, cryptopanic_config

    # News Downloader object
    news_downloader = NewsDownloader(cryptopanic_api_key=cryptopanic_config.api_key)

    # Quix Streams data source that wraps the news downloader
    news_source = NewsDataSource(
        news_downloader=news_downloader,
        polling_interval_sec=config.polling_interval_sec,
    )

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        news_source=news_source,
    )
