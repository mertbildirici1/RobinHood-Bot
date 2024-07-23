import os
import time
from dotenv import load_dotenv
import robin_stocks.robinhood as rh
import pandas as pd
import numpy as np
from bot import fetch_historical_data, buy_stock, sell_stock

positions = {
    'symbol1': 0,
    'symbol2': 0
}

def trade_pairs(df, symbol1, symbol2, entry_threshold, exit_threshold):
    for index, row in df.iterrows():
        if row['zscore'] > entry_threshold and positions['symbol1'] <= 0 and positions['symbol2'] >= 0:
            sell_stock(symbol1, 1)
            buy_stock(symbol2, 1)
            positions['symbol1'] -= 1
            positions['symbol2'] += 1
            print(f"Pair trade executed: Short {symbol1}, Long {symbol2} on {index}")
        elif row['zscore'] < -entry_threshold and positions['symbol1'] >= 0 and positions['symbol2'] <= 0:
            buy_stock(symbol1, 1)
            sell_stock(symbol2, 1)
            positions['symbol1'] += 1
            positions['symbol2'] -= 1
            print(f"Pair trade executed: Long {symbol1}, Short {symbol2} on {index}")
        elif abs(row['zscore']) < exit_threshold:
            if positions['symbol1'] < 0 and positions['symbol2'] > 0:
                buy_stock(symbol1, abs(positions['symbol1']))
                sell_stock(symbol2, abs(positions['symbol2']))
                positions['symbol1'] = 0
                positions['symbol2'] = 0
                print(f"Exit signal on {index} with zscore {row['zscore']} - Exited short {symbol1}, long {symbol2}")
            elif positions['symbol1'] > 0 and positions['symbol2'] < 0:
                sell_stock(symbol1, abs(positions['symbol1']))
                buy_stock(symbol2, abs(positions['symbol2']))
                positions['symbol1'] = 0
                positions['symbol2'] = 0
                print(f"Exit signal on {index} with zscore {row['zscore']} - Exited long {symbol1}, short {symbol2}")