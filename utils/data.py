import yfinance as yf
import pandas as pd

def get_realtime_price(ticker):
    data = yf.Ticker(ticker)
    price = data.history(period="1d", interval="1m")["Close"].iloc[-1]
    return float(price)

def get_historical_data(ticker, interval="1m", lookback="5d"):
    data = yf.download(ticker, period=lookback, interval=interval, progress=False)
    return data
