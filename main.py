import time

import requests
import logging
from exchanges.binance import BinanceClient
from data_collector import collect_all
import strategies
import pattern

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("info.txt")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

if __name__ == "__main__":
    mode = input("chose the program ").lower()
    client = BinanceClient(False)

    symbol = input("Enter the input :: ").upper()

    while True:
        if symbol in client.symbols:
            break
        else:
            print("invalid symbol")
            symbol = input("Enter the input :: ").upper()

    if mode == "data":
        logger.info("Entering data collection mode")
        collect_all(client, symbol)

    elif mode == "test":
        strategy = ["bb","sma","macd","obv","rsi"]
        print(strategy)
        type = input("Chose the strategy :: ")

        while True:
            if type in strategy:
                break
            else:
                print("wrong input")
                type = input("Chose the strategy :: ")

        days = int(input("Enter number of days to go back :: "))
        tf = input("Enter Time format :: ")
        if type == "bb":
            tp = int(input("Enter period :: "))
            strategies.bollinger_band(symbol, tp, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000),
                                      int(time.time() * 1000))

        if type == "macd":
            fast_period = int(input("Enter fast period :: "))
            slow_period = int(input("Enter slow period :: "))
            signal_period = int(input("Enter signal period :: "))
            strategies.macd(symbol, fast_period, slow_period, signal_period, tf,
                            int(time.time() * 1000 - days * 24 * 60 * 60 * 1000), int(time.time() * 1000))

        if type =="obv":
            strategies.obv(symbol, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000), int(time.time() * 1000))

        if type =="sma":
            fastest =  int(input("Enter fastest period :: "))
            medium = int(input("Enter medium period :: "))
            longest = int(input("Enter longest  period :: "))
            strategies.sma_cross(symbol, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000),
                                 int(time.time() * 1000), fastest, medium, longest)


        if type =="rsi":
            period =  int(input("Enter period :: "))

            strategies.rsi(symbol, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000),
                                 int(time.time() * 1000),period)


        #fastest =  int(input("Enter fastest period :: "))
        #medium = int(input("Enter medium period :: "))
        #longest = int(input("Enter longest  period :: "))

        #strategies.bollinger_band(symbol, tp, tf, int(time.time() * 1000 - days*24*60*60*1000), int(time.time() * 1000))



        #strategies.obv(symbol,tf,int(time.time() * 1000 - days*24*60*60*1000),int(time.time() * 1000))

        #strategies.sma_cross(symbol,tf,int(time.time() * 1000 - days*24*60*60*1000),int(time.time() * 1000),fastest,medium,longest)

    elif mode == "pattern":
        days = int(input("Enter number of days to go back :: "))
        tf = input("Enter Time format :: ")

        patterns = ["evening star","hammer","engulfing","three black crows","three line strike"]
        print(patterns)
        type = input("Chose the pattern :: ")

        while True:
            if type in patterns:
                break
            else:
                print("wrong input")
                type = input("Chose the pattern:: ")

        if type == "evening star":
            pattern.evening_star(symbol, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000),
                                 int(time.time() * 1000))
        if type == "hammer":
            pattern.hammer(symbol, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000), int(time.time() * 1000))

        if type == "engulfing":
            pattern.engulfing(symbol, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000), int(time.time() * 1000))

        if type == "three black crows":
            pattern.three_crows(symbol, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000), int(time.time() * 1000))

        if type == "three line strike":
            pattern.three_strike(symbol, tf, int(time.time() * 1000 - days * 24 * 60 * 60 * 1000), int(time.time() * 1000))


        #pattern.evening_star(symbol,tf,int(time.time() * 1000 - days*24*60*60*1000),int(time.time() * 1000))

