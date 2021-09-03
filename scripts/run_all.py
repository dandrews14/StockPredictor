import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

import calculate_current_holdings as cur
import calculate_SandP500 as sp500
import calculate_with_closing_data_curr_holdings as close_cur
import calculate_with_closing_data_sandp500 as close_500
import calculate_without_sma as no_sma

if __name__ == "__main__":
  cur.calculate_scores()
  sp500.calculate_scores()
  close_cur.calculate_scores()
  close_500.calculate_scores()
  no_sma.calculate_scores()
