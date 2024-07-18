import json
import os
from dotenv import load_dotenv
import robin_stocks.robinhood as rh

# Load environment variables from .env file
load_dotenv()

username = os.getenv('ROBINHOOD_USERNAME')
password = os.getenv('ROBINHOOD_PASSWORD')
rh.login(username, password)

account_info = rh.account.load_phoenix_account()
# print(account_info)
account_info_json = json.dumps(account_info)

print(json.dumps(account_info, indent=4))