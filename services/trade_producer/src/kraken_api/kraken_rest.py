from typing import Dict, List

import json
import requests
from loguru import logger


class KrakenRestAPI:

    def __init__(
        self,
        pairs: List[str],
        from_timestamp: int,
        to_timestamp: int,
    ) -> None:
        """
        Initializes Kraken REST API.

        Args:
            pairs (List[str]): List of trade pairs to get trades from.
            from_timestamp (int): The timestamp (in milliseconds) to start getting trades from.
            to_timestamp (int): The timestamp (in milliseconds) to stop getting trades from.

        Returns:
            None
        """
        self.pairs = pairs
        self.from_timestamp = from_timestamp
        self.to_timestamp = to_timestamp

        #TODO: chnage this to get multiple pairs.
        self.URL = f'https://api.kraken.com/0/public/Trades?pair={self.pairs[0]}&since={self.from_timestamp // 1000}' # covert from_timestamp to seconds
        self.is_done = False

    def get_trades(self) -> List[Dict]:
        """
        Gets trade pairs from Kraken REST API and returns them as a list of dictionaries.

        Args:
            pairs (List[str]): List of trade pairs to get trades from.
            from_timestamp (int): The timestamp to start getting trades from.
            to_timestamp (int): The timestamp to stop getting trades from.

        Returns:
            List[Dict]: List of trades.
        """

        payload = {}
        headers = {'Accept': 'application/json'}
        response = requests.request('GET', self.URL, headers=headers, data=payload)

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


        last_timestamp = int(response['result']['last']) // 1_000_000 # convert nanoseconds to milliseconds
        if last_timestamp >= self.to_timestamp:
            self.is_done = True

        logger.info(f'feteched {len(trades)} trades from Kraken API.')

        logger.info(f'last timestamp: {last_timestamp}')

        print(self.from_timestamp)

        return trades

    def done(self) -> bool:
        # TODO: this is just a placeholder for now. Change this to return True when done getting historical data.
        return False
