import json
import os
from dotenv import load_dotenv
import robin_stocks.robinhood as rh
import pandas as pd
import numpy as np

# Load environment variables from .env file
load_dotenv()

username = os.getenv('ROBINHOOD_USERNAME')
password = os.getenv('ROBINHOOD_PASSWORD')
rh.login(username, password)

account_info = rh.account.load_phoenix_account()
# print(account_info)
account_info_json = json.dumps(account_info)

# print(json.dumps(account_info, indent=4))

def buy_stock(symbol, quantity):
    try:
        # Place a market buy order
        order = rh.orders.order_buy_market(symbol, quantity)
        print(f"Order placed: {order}")
    except Exception as e:
        print(f"Error placing order: {e}")

symbol = 'DRIV'
quantity = 1

buy_stock(symbol, quantity)


def fetch_historical_data(symbol, interval, span):
    historicals = rh.stocks.get_stock_historicals(symbol, interval=interval, span=span)
    df = pd.DataFrame(historicals)
    df['begins_at'] = pd.to_datetime(df['begins_at'])
    df.set_index('begins_at', inplace=True)
    df['close_price'] = df['close_price'].astype(float)
    df['close_price'] = df['close_price'].round(2)
    return df

symbol = 'AAPL' 
interval = 'day'
span = '5year'
df = fetch_historical_data(symbol, interval, span)

# Print the last 5 rows of the DataFrame
#print(df.tail().to_string())

# Save the DataFrame to a CSV file
# df.tail().to_csv('/Users/mertbildirici/Desktop/RobinHood Bot/historical_data1.csv')
