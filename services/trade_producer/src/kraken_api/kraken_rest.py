import json
from typing import Dict, List, Tuple
from datetime import datetime, timezone
import requests
from loguru import logger


class KrakenRestAPI:
    def __init__(
        self,
        pairs: List[str],
        last_n_days: int,
    ) -> None:
        """
        Initializes Kraken REST API.

        Args:
            pairs (List[str]): List of trade pairs to get trades from.
            last_n_days (int): The number of days to get historical data.

        Returns:
            None
        """
        self.pairs = pairs
        self.from_timestamp, self.to_timestamp = self._dateTime(last_n_days)

        logger.debug(
            f'Initializing Kraken REST API with pairs: {pairs} and timestamps: {self.from_timestamp} - {self.to_timestamp}.'
        )

        # TODO: chnage this to get multiple pairs.
        self.URL = (
            'https://api.kraken.com/0/public/Trades?pair={product_id}&since={since_sec}'
        )
        self._is_done = False
        self.last_trade_ms = self.from_timestamp

    def get_trades(self) -> List[Dict]:
        """
        Gets trade pairs from Kraken REST API and returns them as a list of dictionaries.

        Returns:
            List[Dict]: List of trades.
        """

        payload = {}
        headers = {'Accept': 'application/json'}

        since_sec = self.last_trade_ms // 1000  # convert milliseconds to seconds
        url = self.URL.format(product_id=self.pairs[0], since_sec=since_sec)

        response = requests.request('GET', url, headers=headers, data=payload)

        response = json.loads(response.text)

        # check for errors in Kraken API response
        if response['error'] != []:
            raise Exception(response['error'])

        # get price, volume, and timestamp from response
        trades = [
            {
                'price': float(trade[0]),
                'volume': float(trade[1]),
                'timestamp': int(trade[2]),
                'product_id': self.pairs[0],
            }
            for trade in response['result'][self.pairs[0]]
        ]

        # filter trades that are outside the timestamp range
        trades = [
            trade for trade in trades if trade['timestamp'] <= self.to_timestamp // 1000
        ]

        last_timestamp_ns = int(response['result']['last'])

        # Update last trade timestamp to the last trade timestamp in the response
        self.last_trade_ms = last_timestamp_ns // 1_000_000
        self._is_done = self.last_trade_ms >= self.to_timestamp

        logger.info(f'fetched {len(trades)} trades from Kraken API.')
        logger.info(f'last timestamp: {self.last_trade_ms}')

        return trades

    def done(self) -> bool:
        # TODO: this is just a placeholder for now. Change this to return True when done getting historical data.
        return self._is_done

    @staticmethod
    def _dateTime(last_n_days) -> Tuple[int, int]:
        today_date = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        # today_date to milliseconds
        to_timestamp = int(today_date.timestamp() * 1000)

        # from_ms is last_n_days ago from today, so
        from_timestamp = to_timestamp - last_n_days * 24 * 60 * 60 * 1000
        return (from_timestamp, to_timestamp)
