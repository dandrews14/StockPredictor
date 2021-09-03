import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

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
    ans['price'] = price_data
    return ans

def volatility(price_data):
    ans = pd.DataFrame(0, index=price_data.index, columns=['price', 'volatility'])
    ans['price'] = price_data
    ans['volatility'] = price_data.rolling(window=10).std()
    return ans



def calculate_scores():
    f = open("../stock_data/sandp500.txt", "r")
    symbols = f.read().splitlines()
    f.close()
    
    scores = []
    for symbol in symbols:
        data = yf.Ticker(symbol)
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

        mean_vol = stock_vol["volatility"].mean()
        flag = 0
        last_price = stock_sma.ix[-2,'price']
        current_price = stock_sma.ix[-1,'price']

        # Bollinger Calculation
        upper_band = stock_boll.ix[-1,'upper_band']
        lower_band = stock_boll.ix[-1,'lower_band']
        bp = stock_boll.ix[-1,'bp']

        if (last_price >= upper_band) and (current_price <= upper_band):
            flag -= 1
        elif (last_price <= lower_band) and (current_price >= lower_band):
            flag += 1

        if (last_price >= current_price) and (bp >= 70):
            flag -= bp/100
        elif (last_price <= current_price) and (bp <= 30):
            flag += (100-bp)/100

        # SMA
        current_SMA = stock_sma.ix[-1,'sma']
        if (last_price >= current_SMA) and (current_price <= current_SMA):
            flag -= 1
        elif (last_price <= current_SMA) and (current_price >= current_SMA):
            flag += 1

        # Volatility
        curr_vol = stock_vol.ix[-1,'volatility']
        vol_score = (mean_vol-curr_vol)/(mean_vol*2)
        flag += vol_score
        entry = (symbol, flag)
        scores.append(entry)
        scores = sorted(scores, reverse=True, key=lambda x:x[1])

    res_string = ""
    for i in scores[:8]:
        res_string += i[0]
        res_string += ", "
        res_string += str(round(i[1], 2))
        res_string += "\n"
                
    
    f = open("../outputs/Top_Stock_Scores.txt", "w")
    f.write(res_string)
    f.close()
    
    f = open("../outputs/All_sandp500_scores.txt", "w")
    res_string = ""
    for i in scores:
        res_string += i[0]
        res_string += ", "
        res_string += str(round(i[1], 2))
        res_string += "\n"
        
    f.write(res_string)
    f.close()


