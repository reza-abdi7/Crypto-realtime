from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(kafka_broker_address: str, kafka_topic: str, kraken_api: KrakenWebsocketAPI):
    """
    reads trades from the kraken API and push them to kafka topics.

    it does 2 things:
    1. reads trades from the kraken API
    2. push the trades to kafka topic.

    Args:
        kafka_broker_address (str): the address of the kafka broker
        kafka_topic (str): the topic to push the trades to
        kraken_api (KrakenWebsocketAPI): the kraken api to read trades from
    Returns:
        None
    """
    logger.info('Starting trades service')

    # initialize the quixstreams application
    # this class will handle the low-level details to connect to kafka.
    app = Application(broker_address=kafka_broker_address)

    # Define a topic where the trades will be pushed
    topic = app.topic(name=kafka_topic, value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()

            for trade in trades:
                # serialize the trade to json
                message = topic.serialize(
                    key=trade.pair.replace('/', '-'),
                    value=trade.to_dict(),
                )

                # push the serialized message to the topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Pushed trade {trade} to topic {kafka_topic}')


if __name__ == '__main__':
    from config import config

    # initialize the kraken api
    kraken_api = KrakenWebsocketAPI(config.pairs)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        kraken_api=kraken_api,
    )
