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

# % Bollinger Bands
# %B = (Price - Lower Band)/(Upper Band - Lower Band)
def bollinger_bands(price_data):
    # zeroed = price_data/price_data[0]
    ans = pd.DataFrame(0, index=price_data.index, columns=['upper_band', 'lower_band', 'price', 'bp'])
    rolling_mean = price_data.rolling(window=20).mean()
    standard_dev = price_data.rolling(window=20).std()
    ans['upper_band'] = rolling_mean + (2*standard_dev)
    ans['lower_band'] = rolling_mean - (2*standard_dev)

    ans['bp'] = (price_data - ans['lower_band'])/(ans['upper_band']-ans['lower_band'])*100
    #print(ans['bp'])
    ans['price'] = price_data
    #print(ans['price'])
    #print(ans['bp'])
    return ans

def volatility(price_data):
    ans = pd.DataFrame(0, index=price_data.index, columns=['price', 'volatility'])
    ans['price'] = price_data
    ans['volatility'] = price_data.rolling(window=10).std()
    #print(ans)
    return ans



def calculate_scores():
    f = open("./current_holdings.txt", "r")
    #f = open("./stock_data/fiels/all_stocks.txt", "r")
    symbols = f.read().splitlines()
    f.close()
    #print(symbols)
    
    for i in range(len(symbols)):
        symbols[i] = symbols[i].split(",")[0]


    #symbols = ['DWSH']
    scores = []
    #print('Here')
    for symbol in symbols:
        # Get Data for Symbol
        data = yf.Ticker(symbol)
        #print("HERE")

        filename = symbol

        tickdf = data.history(period='1d',start=datetime.today()- timedelta(days=90), end=datetime.today())
        try:
            error_message = yf.shared._ERRORS[symbol]
            #print(error_message)
            continue
        except:
            pass
        #print(tickdf['Open']) 
        # Calculate Statistics
        #print(symbol)
        #print(tickdf.shape)

        if tickdf.shape[0] < 30:
            print(symbol)
            continue
        stock_vol = volatility(tickdf['Open'])
        stock_boll = bollinger_bands(tickdf['Open'])
        stock_sma = sma(tickdf['Open'])
        #print("#### this far #####")
        #print(stock_boll)
        fig = stock_sma.plot()

        fig = fig.get_figure()
        fig.savefig("./plots/" + filename + "_sma.png")


calculate_scores()

