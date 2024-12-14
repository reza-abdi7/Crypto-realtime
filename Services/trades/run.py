from kraken_api.base import TradesAPI
from kraken_api.rest import KrakenRestAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(kafka_broker_address: str, kafka_topic: str, trades_api: TradesAPI):
    """
    reads trades from the kraken API and push them to kafka topics.

    it does 2 things:
    1. reads trades from the kraken API
    2. push the trades to kafka topic.

    Args:
        kafka_broker_address (str): the address of the kafka broker
        kafka_topic (str): the topic to push the trades to
        kraken_api (TradesAPI) with 2 methods: get_trades() and is_done()
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
        while not trades_api.is_done():
            trades = trades_api.get_trades()

            for trade in trades:
                # serialize the trade to json
                message = topic.serialize(
                    key=trade.pair.replace('/', '-'),
                    value=trade.to_dict(),
                )

                # push the serialized message to the topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Pushed trade to topic {kafka_topic}')


if __name__ == '__main__':
    from config import config

    # initialize the kraken api depending on the data source
    if config.data_source == 'live':
        kraken_api = KrakenWebsocketAPI(config.pairs)
    elif config.data_source == 'historical':
        kraken_api = KrakenRestAPI(config.pairs, last_n_days=config.last_n_days)
    else:
        raise ValueError(f'Unknown data source: {config.data_source}')

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        trades_api=kraken_api,
    )
