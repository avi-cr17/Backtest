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



def evening_star(symbol :str ,format:str, start : int, end : int):
    df = get_df(symbol, format, start, end)
    values = talib.CDLEVENINGSTAR(open = df["open"], high = df["high"], low = df["low"], close = df["close"], penetration=0)
    df["values"]=values

    df["bullish"] = df["values"]
    df.loc[df['values'] == -100, "bullish"] = None
    df.loc[df['values'] == -200, "bullish"] = None
    df.loc[df['values'] == 0, "bullish"] = None
    df.loc[df['values'] == 100, "bullish"] = 0.97 * df["low"]
    df.loc[df['values'] == 200, "bullish"] = df["low"]

    df["bearish"] = df["values"]
    df.loc[df['values'] == 100, "bearish"] = None
    df.loc[df['values'] == 200, "bearish"] = None
    df.loc[df['values'] == 0, "bearish"] = None
    df.loc[df['values'] == -100, "bearish"] = 1.07 * df["high"]
    df.loc[df['values'] == -200, "bearish"] = df["high"]


    fg = go.Figure(go.Candlestick(x=df.index,
                                  open=df["open"],
                                  high=df["high"],
                                  low=df["low"],
                                  close=df["close"]))

    fg.add_trace(go.Scatter(x=df.index, y=df["bullish"], mode='markers', marker=dict(
        color='LightSkyBlue',
        size=12,
    )))

    fg.add_trace(go.Scatter(x=df.index, y=df["bearish"], mode='markers', marker=dict(
        color='Violet',
        size=12,
    )))
    fg.update_layout(xaxis_rangeslider_visible=False)
    fg.show()
    print(df)

def hammer(symbol :str ,format:str, start : int, end : int):
    df = get_df(symbol, format, start, end)
    values = talib.CDLHAMMER(open = df["open"], high = df["high"], low = df["low"], close = df["close"])
    df["values"] = values
    print(df)

    fg = go.Figure(go.Candlestick(x=df.index,
                                  open=df["open"],
                                  high=df["high"],
                                  low=df["low"],
                                  close=df["close"]))

    df["bullish"] = df["values"]
    df.loc[df['values'] == -100, "bullish"] = None
    df.loc[df['values'] == -200, "bullish"] = None
    df.loc[df['values'] == 0,"bullish"] = None
    df.loc[df['values'] == 100,"bullish"] = 0.97*df["low"]
    df.loc[df['values'] == 200,"bullish"] = df["low"]

    df["bearish"] = df["values"]
    df.loc[df['values'] == 100, "bearish"] = None
    df.loc[df['values'] == 200, "bearish"] = None
    df.loc[df['values'] == 0, "bearish"] = None
    df.loc[df['values'] == -100, "bearish"] = 1.07*df["high"]
    df.loc[df['values'] == -200, "bearish"] = df["high"]



    fg.add_trace(go.Scatter(x=df.index,y=df["bullish"], mode='markers', marker=dict(
            color='LightSkyBlue',
            size=12,
        )))

    fg.add_trace(go.Scatter(x=df.index, y=df["bearish"], mode='markers', marker=dict(
        color='Violet',
        size=12,
    )))
    fg.update_layout(xaxis_rangeslider_visible=False)
    fg.show()


def engulfing(symbol :str ,format:str, start : int, end : int):
    df = get_df(symbol, format, start, end)
    values = talib.CDLENGULFING(open = df["open"], high = df["high"], low = df["low"], close = df["close"])
    df["values"] = values
    print(df)

    fg = go.Figure(go.Candlestick(x=df.index,
                                  open=df["open"],
                                  high=df["high"],
                                  low=df["low"],
                                  close=df["close"]))

    df["bullish"] = df["values"]
    df.loc[df['values'] == -100, "bullish"] = None
    df.loc[df['values'] == -200, "bullish"] = None
    df.loc[df['values'] == 0,"bullish"] = None
    df.loc[df['values'] == 100,"bullish"] = 0.97*df["low"]
    df.loc[df['values'] == 200,"bullish"] = df["low"]

    df["bearish"] = df["values"]
    df.loc[df['values'] == 100, "bearish"] = None
    df.loc[df['values'] == 200, "bearish"] = None
    df.loc[df['values'] == 0, "bearish"] = None
    df.loc[df['values'] == -100, "bearish"] = 1.07*df["high"]
    df.loc[df['values'] == -200, "bearish"] = df["high"]



    fg.add_trace(go.Scatter(x=df.index,y=df["bullish"], mode='markers', marker=dict(
            color='LightSkyBlue',
            size=12,
        )))

    fg.add_trace(go.Scatter(x=df.index, y=df["bearish"], mode='markers', marker=dict(
        color='Violet',
        size=12,
    )))
    fg.update_layout(xaxis_rangeslider_visible=False)
    fg.show()


def three_crows(symbol :str ,format:str, start : int, end : int):
    df = get_df(symbol, format, start, end)
    values = talib.CDL3BLACKCROWS(open = df["open"], high = df["high"], low = df["low"], close = df["close"])
    df["values"] = values
    print(df)

    fg = go.Figure(go.Candlestick(x=df.index,
                                  open=df["open"],
                                  high=df["high"],
                                  low=df["low"],
                                  close=df["close"]))

    df["bullish"] = df["values"]
    df.loc[df['values'] == -100, "bullish"] = None
    df.loc[df['values'] == -200, "bullish"] = None
    df.loc[df['values'] == 0,"bullish"] = None
    df.loc[df['values'] == 100,"bullish"] = 0.97*df["low"]
    df.loc[df['values'] == 200,"bullish"] = df["low"]

    df["bearish"] = df["values"]
    df.loc[df['values'] == 100, "bearish"] = None
    df.loc[df['values'] == 200, "bearish"] = None
    df.loc[df['values'] == 0, "bearish"] = None
    df.loc[df['values'] == -100, "bearish"] = 1.07*df["high"]
    df.loc[df['values'] == -200, "bearish"] = df["high"]



    fg.add_trace(go.Scatter(x=df.index,y=df["bullish"], mode='markers', marker=dict(
            color='LightSkyBlue',
            size=12,
        )))

    fg.add_trace(go.Scatter(x=df.index, y=df["bearish"], mode='markers', marker=dict(
        color='Violet',
        size=12,
    )))
    fg.update_layout(xaxis_rangeslider_visible=False)
    fg.show()

def three_strike(symbol :str ,format:str, start : int, end : int):
    df = get_df(symbol, format, start, end)
    values = talib.CDL3LINESTRIKE(open = df["open"], high = df["high"], low = df["low"], close = df["close"])
    df["values"] = values
    print(df)

    fg = go.Figure(go.Candlestick(x=df.index,
                                  open=df["open"],
                                  high=df["high"],
                                  low=df["low"],
                                  close=df["close"]))

    df["bullish"] = df["values"]
    df.loc[df['values'] == -100, "bullish"] = None
    df.loc[df['values'] == -200, "bullish"] = None
    df.loc[df['values'] == 0,"bullish"] = None
    df.loc[df['values'] == 100,"bullish"] = 0.97*df["low"]
    df.loc[df['values'] == 200,"bullish"] = df["low"]

    df["bearish"] = df["values"]
    df.loc[df['values'] == 100, "bearish"] = None
    df.loc[df['values'] == 200, "bearish"] = None
    df.loc[df['values'] == 0, "bearish"] = None
    df.loc[df['values'] == -100, "bearish"] = 1.07*df["high"]
    df.loc[df['values'] == -200, "bearish"] = df["high"]



    fg.add_trace(go.Scatter(x=df.index,y=df["bullish"], mode='markers', marker=dict(
            color='LightSkyBlue',
            size=12,
        )))

    fg.add_trace(go.Scatter(x=df.index, y=df["bearish"], mode='markers', marker=dict(
        color='Violet',
        size=12,
    )))
    fg.update_layout(xaxis_rangeslider_visible=False)
    fg.show()