import json
import time
from typing import List

import requests
from loguru import logger

from .base import TradesAPI
from .trade import Trade


class KrakenRestAPI(TradesAPI):
    def __init__(self, pairs: List[str], last_n_days: int):
        self.pairs = pairs

        self.apis = [
            KrakenRestAPISinglePair(pair=pair, last_n_days=last_n_days)
            for pair in self.pairs
        ]

    def get_trades(self) -> List[Trade]:
        """
        get trades for each pari, sort them by timestamp and return trades.
        """
        trades = []
        for api in self.apis:
            if not api.is_done():
                trades += api.get_trades()

        # sort trades by timestamp
        trades.sort(key=lambda x: x.timestamp_ms)

        breakpoint()

        return trades

    def is_done(self) -> bool:
        """
        we are done when all apis are done
        """
        for api in self.apis:
            if not api.is_done():
                return False
        return True


class KrakenRestAPISinglePair(TradesAPI):
    URL = 'https://api.kraken.com/0/public/Trades'

    def __init__(
        self,
        pair: str,
        last_n_days: int,
    ):
        self.pair = pair
        self.last_n_days = last_n_days
        self._is_done = False
        # get current timestamp in nanoseconds
        self.since_timestamp_ns = int(
            (time.time() - self.last_n_days * 24 * 60 * 60) * 1_000_000_000
        )

        logger.info(
            f'Getting trades for pair {self.pair} for the last {self.last_n_days} days'
        )

    def get_trades(self) -> List[Trade]:
        """
        Sends a request to the Kraken API and returns the trades for the pair.
        Returns:
            List[Trade]: A list of Trade objects
        """
        headers = {'Accept': 'application/json'}
        params = {'pair': self.pair, 'since': self.since_timestamp_ns}

        response = requests.request('GET', self.URL, params=params, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.text)

        else:
            logger.error(f'Request failed with status code {response.status_code}')
            return []

        # get the trades for the self.pair cryptocurrency
        try:
            trades = data['result'][self.pair]
        except KeyError as e:
            logger.error(f'Failed to get trades for pair {self.pair}: {e}')
            return []

        # convert the trades to trade objects
        trades = [
            Trade.from_kraken_rest_api_response(
                pair=self.pair,
                price=float(trade[0]),
                volume=float(trade[1]),
                timestamp_sec=trade[2],
            )
            for trade in trades
        ]

        # update the since_timestamp_ns variable
        self.since_timestamp_ns = float(data['result']['last'])

        # check if we are done
        # TODO: check if this stopping conditions really work
        if self.since_timestamp_ns > int(time.time() * 1_000_000_000 - 1000000000):
            self._is_done = True
        if self.since_timestamp_ns == 0:
            self._is_done = True

        # breakpoint()
        return trades

    def is_done(self) -> bool:
        return self._is_done
