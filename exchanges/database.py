import h5py
from typing import *
import numpy as np
import logging
import pandas as pd

pd.set_option("display.max_rows",50)
logger = logging.getLogger()


class HDF5database:
    def __init__(self):
        self.hf = h5py.File("database.h5", "a")
        self.hf.flush()

    def create_database(self, symbol: str):
        if symbol not in self.hf.keys():
            self.hf.create_dataset(symbol, (0, 6), maxshape=(None, 6), dtype="float64")
            self.hf.flush()

    def data_read(self, symbol: str, start: int, end: int):
        data = self.hf[symbol][:]

        if len(data) == 0:
            return
        # print(data)
        data = sorted(data, key=lambda x: x[0])
        data = np.array(data)
        # print(data)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        df = df[(df['timestamp'] >= start) & (df['timestamp'] <= end)]
        df['timestamp'] = pd.to_datetime(df['timestamp'].values.astype(np.int64), unit='ms')
        df.set_index('timestamp', drop=True, inplace=True)
        return df

    def write_data(self, symbol: str, data: List[Tuple]):

        oldest, newest = self.last_and_first(symbol)

        if oldest is None:
            oldest = float("inf")
        if newest is None:
            newest = 0

        filtered_data = []
        # print("write",data) works

        for d in data:
            if d[0] < oldest:
                filtered_data.append(d)
            elif d[0] > newest:
                filtered_data.append(d)

        if filtered_data is None:
            logger.warning("%s no data found", symbol)
            return

        data_np = np.array(filtered_data)
        # print("write2",data_np) works
        self.hf[symbol].resize(self.hf[symbol].shape[0] + data_np.shape[0], axis=0)
        self.hf[symbol][-data_np.shape[0]:] = data_np
        # print("database write",self.hf[symbol][:]) works
        self.hf.flush()

    def last_and_first(self, symbol: str):

        data = self.hf[symbol][:]

        if len(data) == 0:
            return None, None
        else:
            oldest = min(data, key=lambda x: x[0])[0]
            recent = max(data, key=lambda x: x[0])[0]
            return oldest, recent

    def resample_timeframe(self, data: pd.DataFrame, timeframe: str):

        return data.resample(timeframe).agg(
            {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
        )
