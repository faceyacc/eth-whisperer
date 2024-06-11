from typing import List, Dict
from websocket import create_connection
import json

class KrakenWebsocketTradeAPI:
    URL = 'wss://ws.kraken.com/v2'

    def __init__(self, product_id) -> None:
        self.product_id = product_id

        # Establish connection to Kraken Websocket.
        self._ws = create_connection(url=self.URL)
        print("connection to Kraken successful!")

        # Subscribe to trades.
        self._subscribe(product_id=product_id)




    def _subscribe(self, product_id) -> None:
        """
        Established an connection to Kraken Websocket API and subscribes to
        to trades given product_id.

        Args:
            product_id (str): trade pair ticker.

        Returns:
            None
        """

        # Subscribe to Kraken trades
        print("subscribing to trades...")
        msg = {
            "method": "subscribe",
            "params": {
                "channel": "trade",
                "symbol": [
                    product_id
                ],
                "snapshot": False
            }
        }

        self._ws.send(json.dumps(msg))
        print("subscription worked!")


        # Dumping first two messages from Kraken.
        _ = self._ws.recv()
        _ = self._ws.recv()



    def get_trades(self) -> List[Dict]:
        msg = self._ws.recv()

        if 'heartbeat' in str(msg):
            return []

        msg = json.loads(msg)


        # Structure trade from message data.
        trades = []
        for trade in msg['data']:
            trades.append({
                'product_id': self.product_id,
                'price': trade['price'],
                'volume': trade['qty'],
                'timestamp': trade['timestamp']
            })


        return trades
