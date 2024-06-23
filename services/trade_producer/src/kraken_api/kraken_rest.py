from typing import Dict, List

import requests


class KrakenRestAPI:
    # URL = 'https://api.kraken.com/0/public/Trades'

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
        self.URL = f'https://api.kraken.com/0/public/Trades?pair={pairs[0]}&since{from_timestamp}'

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

        print(response.text)

        breakpoint()

        return []

    def done(self) -> bool:
        # TODO: this is just a placeholder for now. Change this to return True when done getting historical data.
        return False
