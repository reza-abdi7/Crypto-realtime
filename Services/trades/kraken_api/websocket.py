import json
from typing import List

import websocket
from loguru import logger
from websocket import create_connection

from .base import TradesAPI
from .trade import Trade


class KrakenWebsocketAPI(TradesAPI):
    URL = 'wss://ws.kraken.com/v2'

    def __init__(self, pairs: List[str]):
        self.pairs = pairs
        websocket.enableTrace(True)
        logger.info(f'Connecting to Kraken Websocket with pairs: {self.pairs}')
        self._ws_client = create_connection(url=self.URL)
        self._subscribe()

    def _subscribe(self):
        """
        subscribe to the websocket and handle initial subscription messages
        """
        # send a subscribe message to the websocket
        subscribe_msg = {
            'method': 'subscribe',
            'params': {
                'channel': 'trade',
                'symbol': self.pairs,
                'snapshot': False,
            },
        }
        logger.info(f'Sending subscribe message: {subscribe_msg}')
        self._ws_client.send(json.dumps(subscribe_msg))

        # skip subscription confirmation messages
        for _ in self.pairs:
            msg1 = self._ws_client.recv()
            msg2 = self._ws_client.recv()
            logger.info(f'Subscription confirmation message: {msg1}, {msg2}')

    def get_trades(self) -> List[Trade]:
        """
        Fetches the trades fromm the Kraken Websocket APIs and returns them as a list of Trade objects.

        Returns:
            List[Trade]: A list of Trade objects
        """
        data = self._ws_client.recv()
        logger.info(f'Received message: {data}')

        if 'heartbeat' in data:
            logger.info('Received heartbeat message')
            return []

        # transform raw string into a JSON object
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')
            return []

        try:
            trades_data = data['data']
        except KeyError as e:
            logger.error(f'No data field in message: {e}')
            return []

        trades = [
            Trade.from_kraken_websocket_api_response(
                pair=trade['symbol'],
                price=trade['price'],
                volume=trade['qty'],
                timestamp=trade['timestamp'],
            )
            for trade in trades_data
        ]

        # breakpoint()
        return trades

    def is_done(self) -> bool:
        return False
