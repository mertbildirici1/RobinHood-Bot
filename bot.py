import os
import time
from dotenv import load_dotenv
import robin_stocks.robinhood as rh
import pandas as pd
import numpy as np

load_dotenv()

username = os.getenv('ROBINHOOD_USERNAME')
password = os.getenv('ROBINHOOD_PASSWORD')
rh.login(username, password)
account_info = rh.account.load_phoenix_account()

def buy_stock(symbol, quantity):
    try:
        order = rh.orders.order_buy_market(symbol, quantity)
        print(f"Order placed: {order}")
    except Exception as e:
        print(f"Error placing order: {e}")

def sell_stock(symbol, quantity):
    try:
        order = rh.orders.order_sell_market(symbol, quantity)
        print(f"Order placed: {order}")
    except Exception as e:
        print(f"Error placing order: {e}")

def fetch_historical_data(symbol, interval, span):
    historicals = rh.stocks.get_stock_historicals(symbol, interval=interval, span=span)
    df = pd.DataFrame(historicals)
    df['begins_at'] = pd.to_datetime(df['begins_at'])
    df.set_index('begins_at', inplace=True)
    df['close_price'] = df['close_price'].astype(float)
    df['close_price'] = df['close_price'].round(2)
    return df

def fetch_latest_price(symbol):
    latest_price = rh.stocks.get_latest_price(symbol)
    return float(latest_price[0])

symbol1 = 'AAPL'
symbol2 = 'MSFT'
interval = 'day'
span = '5year'

df1 = fetch_historical_data(symbol1, interval, span)
df2 = fetch_historical_data(symbol2, interval, span)

df1, df2 = df1.align(df2, join='inner', axis=0)

df1['spread'] = df1['close_price'] - df2['close_price']

def zscore(series):
    return (series - series.mean()) / np.std(series)

df1['zscore'] = zscore(df1['spread'])

entry_threshold = 2.0
exit_threshold = 0.5

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

while True:
    try:
        latest_price1 = fetch_latest_price(symbol1)
        latest_price2 = fetch_latest_price(symbol2)
        
        df1.loc[pd.Timestamp.now()] = [latest_price1, latest_price1 - latest_price2, None]
        df1['spread'] = df1['close_price'] - df2['close_price']
        df1['zscore'] = zscore(df1['spread'])
        
        trade_pairs(df1, symbol1, symbol2, entry_threshold, exit_threshold)
        
        time.sleep(3600)
        
    except Exception as e:
        print(f"Error during main loop: {e}")
        break
