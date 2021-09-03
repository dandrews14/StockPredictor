import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def sma(price_data):
    ans = pd.DataFrame(0, index=price_data.index, columns=['price', 'sma'])
    ans['price'] = price_data
    ans['sma'] = price_data.rolling(window=5).mean()
    return ans

def bollinger_bands(price_data):
    ans = pd.DataFrame(0, index=price_data.index, columns=['upper_band', 'lower_band', 'price', 'bp'])
    rolling_mean = price_data.rolling(window=20).mean()
    standard_dev = price_data.rolling(window=20).std()
    ans['upper_band'] = rolling_mean + (2*standard_dev)
    ans['lower_band'] = rolling_mean - (2*standard_dev)

    ans['bp'] = (price_data - ans['lower_band'])/(ans['upper_band']-ans['lower_band'])*100
    ans['price'] = price_data
    return ans

def volatility(price_data):
    ans = pd.DataFrame(0, index=price_data.index, columns=['price', 'volatility'])
    ans['price'] = price_data
    ans['volatility'] = price_data.rolling(window=10).std()
    return ans



def calculate_scores():
    f = open("../stock_data/current_holdings.txt", "r")
    symbols = f.read().splitlines()
    f.close()
    
    for i in range(len(symbols)):
        symbols[i] = symbols[i].split(",")[0]


    scores = []
    for symbol in symbols:
        data = yf.Ticker(symbol)

        filename = symbol

        tickdf = data.history(period='1d',start=datetime.today()- timedelta(days=90), end=datetime.today())
        try:
            error_message = yf.shared._ERRORS[symbol]
            continue
        except:
            pass

        if tickdf.shape[0] < 30:
            print(symbol)
            continue
        stock_vol = volatility(tickdf['Open'])
        stock_boll = bollinger_bands(tickdf['Open'])
        stock_sma = sma(tickdf['Open'])
        fig = stock_sma.plot()

        fig = fig.get_figure()
        fig.savefig("../plots/" + filename + "_sma.png")


calculate_scores()

