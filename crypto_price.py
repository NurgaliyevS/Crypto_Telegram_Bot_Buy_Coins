import requests
from binance.client import Client
import os
import settings
import pandas as pd
from pycoingecko import CoinGeckoAPI
import sqlite3

api_key = os.getenv('binance_api_key')
api_secret = os.getenv('binance_api_secret')

# Authenticate with the client
client = Client(api_key, api_secret)

cg = CoinGeckoAPI()

def get_top_250_coins():
    page = 0
    coin_market = cg.get_coins_markets(vs_currency='usd', per_page=250, page=page)
    df_market = pd.DataFrame(coin_market, columns=['market_cap_rank','id','name','current_price',"price_change_24h","price_change_percentage_24h",'market_cap',"market_cap_change_percentage_24h",'total_volume',  "circulating_supply", "max_supply", "high_24h", "low_24h", ])   
    connect = sqlite3.connect('coins.db')
    df_market.to_sql(name='Coins_Markets', con=connect, if_exists='replace')
    connect.close()

def check_crypto_price(coin):
    try:
        get_top_250_coins()
        sqlite_connection = sqlite3.connect('coins.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        answer = cursor.execute("SELECT cm.id, cm.name, cm.current_price FROM Coins_Markets cm WHERE cm.name = '{}' or cm.id = '{}'".format(coin.capitalize(), coin))
        data = cursor.fetchone()
        cursor.close()
        return data[2]
    except:
        print('Fatality')
    