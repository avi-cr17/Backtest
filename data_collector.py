from exchanges.binance import BinanceClient
import time
import logging
from utils import ms_to_dt
from exchanges.database import HDF5database
import pandas as pd

pd.set_option("display.max_rows", 50)
logger = logging.getLogger()


def collect_all(client: BinanceClient, symbol: str):
    database = HDF5database()
    database.create_database(symbol)
    oldest_ts, latest_ts = database.last_and_first(symbol)

    # if oldest_ts is not None:
    # print(database.data_read(symbol, start=0, end=int(time.time() * 1000)))
    # print(database.resample_timeframe(database.data_read(symbol, start=0, end=int(time.time() * 1000)), "5Min"))

    if oldest_ts is None:
        data = client.get_historical_data(symbol, end_time=int(time.time() * 1000) - 60000)

        if data is None:
            logger.warning("%s  no data found ", symbol)
            return
        else:
            logger.info("%s collected  %s current data sets from %s to %s ", symbol, len(data), ms_to_dt(data[0][0]),
                        ms_to_dt(data[-1][0]))

        oldest_ts = data[0][0]
        latest_ts = data[-1][0]
        # print("initial data",data)
        database.write_data(symbol, data)

    # recent data

    while True:
        data = client.get_historical_data(symbol, start_time=int(latest_ts + 60000))

        if data is None:
            time.sleep(5)
            continue

        if len(data) < 2:
            break

        data = data[:-1]

        logger.info("%s collected %s latest data sets from %s to %s ", symbol, len(data), ms_to_dt(data[0][0]),
                    ms_to_dt(data[-1][0]))

        if data[-1][0] > latest_ts:
            latest_ts = data[-1][0]

        # print("latest data", data)
        database.write_data(symbol, data)
        time.sleep(1.2)

    # older data

    while True:
        data = client.get_historical_data(symbol, end_time=int(oldest_ts - 60000))

        if data is None:
            time.sleep(5)
            continue

        if len(data) == 0:
            break

        logger.info("%s collected %s older data sets from %s to %s ", symbol, len(data), ms_to_dt(data[0][0]),
                    ms_to_dt(data[-1][0]))

        if data[0][0] < oldest_ts:
            oldest_ts = data[0][0]

        # print("older data", data) works
        database.write_data(symbol, data)
        time.sleep(1.2)
