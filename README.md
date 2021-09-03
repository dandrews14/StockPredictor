# Stock Predictor

A simple daily script that can estimate how stocks will perform over the next few days.

## Necesssary Packages:
* Pandas
* NumPy
* yFinance
* Matplotlib

## Instructions:

To run: *python ./<script_name>*

## Additional Information:

* Scripts can be found in the "scripts" directory. Scripts can be used individually or run using "run_all.py"
* Each script generally use three indicators to generate score: Simple Moving Average (SMA), Bollinger Bands (BBP), and the Volatility.
* Scripts can be run on S&P 500 data, NYSE listings data, or a custom holdings data. The .txt files with the stock symbols are in the "stock_data" directory.
* outputs from the scripts are put in the outputs directory.
* Stocks with a score over 1 are generally on the "BUY" side, stocks under -1 are generally on the "SELL" side, all others are "HOLD".
