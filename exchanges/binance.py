import logging

import requests
from typing import *

logger = logging.getLogger()


class BinanceClient:
    def __init__(self, futures=False):

        self.futures = futures

        if self.futures:
            self._base_url = "https://fapi.binance.com"
        else:
            self._base_url = "https://api.binance.com"

        self.symbols = self._get_symbols()

    def _make_request(self, endpoint: str, query_parameters: Dict):

        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)

        except Exception as e:
            logger.error("error wile making requests to %s : %s", endpoint, e)
            return None

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("error wile making requests to %s : %s", endpoint, response.status_code)

            return None

    def _get_symbols(self) -> List[str]:

        params = dict()
        symbols = []

        endpoint = "/fapi/v3/exchangeInfo" if self.futures else "/api/v3/exchangeInfo"
        data = self._make_request(endpoint, params)

        for x in data["symbols"]:
            symbols.append(x["symbol"])

        print(symbols)
        return symbols

    def get_historical_data(self, symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None):
        params = dict()

        params["symbol"] = symbol
        params["interval"] = "1m"
        params["limit"] = 1500

        endpoint = "/fapi/v3/klines" if self.futures else "/api/v3/klines"

        if start_time is not None:
            params["startTime"] = start_time

        if end_time is not None:
            params["endTime"] = end_time

        raw_candles = self._make_request(endpoint, params)

        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                candles.append((float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5]),))
            return candles
        else:
            return None
