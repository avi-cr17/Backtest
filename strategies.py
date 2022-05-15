import talib
import numpy as np
import pandas as pd
import exchanges.database
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.set_option("display.max_rows",None)
pd.set_option("display.max_columns",None)
pd.set_option("display.width",1000)

def get_df(symbol :str ,format:str, start : int, end : int):
    db = exchanges.database.HDF5database()
    df = db.data_read(symbol,start,end)
    df= db.resample_timeframe(data=df,timeframe=format)
    return df


def bollinger_band(symbol:str, period : int , format:str , start: int , end : int):
    df = get_df(symbol,format,start,end)
    upperband, middleband, lowerband = talib.BBANDS(df["close"],timeperiod=period)
    df["upperband"]=upperband
    df["middleband"] = middleband
    df["lowerband"] = lowerband
    fg = go.Figure(go.Candlestick(x=df.index,
                                  open=df["open"],
                                  high=df["high"],
                                  low=df["low"],
                                  close=df["close"]))

    fg.add_trace(go.Line(x=df.index,y=df["upperband"]))
    fg.add_trace(go.Line(x=df.index, y=df["lowerband"]))
    fg.add_trace(go.Line(x=df.index, y=df["middleband"]))
    fg.update_layout(xaxis_rangeslider_visible=False)
    fg.show()
    print(df)

def macd(symbol:str, fast_period : int ,slow_period:int,signal_period :int, format:str , start: int , end : int ):
    df = get_df(symbol,format,start,end)
    macd, macdsignal, macdhist = talib.MACDEXT(df["close"], fastperiod=fast_period, fastmatype=0, slowperiod=slow_period, slowmatype=0, signalperiod=signal_period, signalmatype=0)
    #macd, macdsignal, macdhist = talib.MACDFIX(df["close"],signalperiod=signal_period)
    df["macd"] = macd
    df["macdsignal"] = macdsignal
    df["macdhist"] = macdhist


    fig = make_subplots( rows=2, cols=1, row_heights=[0.6, 0.2])





    fig.add_trace(go.Candlestick(x=df.index,
                                   open=df["open"],
                                   high=df["high"],
                                   low=df["low"],
                                   close=df["close"]))

    fig.add_trace(go.Scatter(x=df.index,y=df["macd"]),row=2,col=1,)
    fig.add_trace(go.Scatter(x=df.index, y=df["macdsignal"]), row=2, col=1,)
    fig.add_trace(go.Bar(x=df.index,y=df["macdhist"]), row=2, col=1, )

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()




    print(df)


def sma_cross(symbol:str, format:str , start: int , end : int, fastest :int , medium : int , longest : int):
    df = get_df(symbol, format, start, end)
    fastest_ma = talib.SMA(df["close"],timeperiod=fastest)
    medium_ma = talib.SMA(df["close"],timeperiod=medium)
    longest_ma =talib.SMA(df["close"],timeperiod=longest)

    df["fastest_ma"] = fastest_ma
    df["medium_ma"] = medium_ma
    df["longest_ma"] = longest_ma

    fg = go.Figure(go.Candlestick(x=df.index,
                                  open=df["open"],
                                  high=df["high"],
                                  low=df["low"],
                                  close=df["close"]))

    fg.add_trace(go.Line(x=df.index, y=df["fastest_ma"]))
    fg.add_trace(go.Line(x=df.index, y=df["medium_ma"]))
    fg.add_trace(go.Line(x=df.index, y=df["longest_ma"]))
    fg.update_layout(xaxis_rangeslider_visible=False)
    fg.show()
    print(df)


def obv(symbol:str, format:str , start: int , end : int):
    df = get_df(symbol, format, start, end)
    obv = talib.OBV(df["close"],df["volume"])
    df["obv"]=obv
    fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4])

    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df["open"],
                                 high=df["high"],
                                 low=df["low"],
                                 close=df["close"]))

    fig.add_trace(go.Scatter(x=df.index, y=df["obv"]), row=2, col=1, )


    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()
    print(df)



def rsi(symbol:str, format:str , start: int , end : int, period : int):
    df = get_df(symbol, format, start, end)
    rsi = talib.RSI(df["close"],timeperiod=period)

    df["rsi"] = rsi

    fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.2])

    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df["open"],
                                 high=df["high"],
                                 low=df["low"],
                                 close=df["close"]))

    fig.add_trace(go.Scatter(x=df.index, y=df["rsi"]), row=2, col=1, )


    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()


    print(df)

    



