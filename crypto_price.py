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

def get_top_100_coins():
    page = 0
    coin_market = cg.get_coins_markets(vs_currency='usd', per_page=250, page=page)
    df_market = pd.DataFrame(coin_market, columns=['market_cap_rank','id','name','current_price',"price_change_24h","price_change_percentage_24h",'market_cap',"market_cap_change_percentage_24h",'total_volume',  "circulating_supply", "max_supply", "high_24h", "low_24h", ])   
    connect = sqlite3.connect('coins.db')
    df_market.to_sql(name='Coins_Markets', con=connect, if_exists='replace')
    connect.close()


def check_crypto_price(coin):
    try:
        get_top_100_coins()
        sqlite_connection = sqlite3.connect('coins.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        answer = cursor.execute("SELECT cm.id, cm.name, cm.current_price FROM Coins_Markets cm WHERE cm.name = '{}' or cm.id = '{}'".format(coin.capitalize(), coin))
        data = cursor.fetchone()
        cursor.close()
        return data[2]
    except:
        print('Fatality')
    
# def check_btc_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_ada_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result

# def check_eth_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result

# def check_bnb_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result

# def check_litecoin_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=LTCUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_solana_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_avalanche_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=AVAXUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_terra_luna_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=LUNAUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result

# def check_ftx_token_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=FTTUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_polkadot_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=DOTUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result

# def check_near_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=NEARUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_uniswap_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=UNIUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_polygon_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=MATICUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_the_graph_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=GRTUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_dogecoin_price():
#     url = 'https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT'
#     resp = requests.get(url)
#     data = resp.json()
#     price = list()
#     price.append(data['price'])
#     result = int()
#     price[0] = float(price[0])
#     for i in price:
#         result += i
#     return result


# def check_price(coin: str):
#     if coin == 'bitcoin':
#         return check_btc_price()

#     elif coin == 'ethereum':
#         return check_eth_price()

#     elif coin == 'binancecoin':
#         return check_bnb_price()

#     elif coin == 'litecoin':
#         return  check_litecoin_price()

#     elif coin == 'solana':
#         return check_solana_price()

#     elif coin == 'avalanche-2':
#         return check_avalanche_price()

#     elif coin == 'terra-luna':
#         return check_terra_luna_price()

#     elif coin == 'ftx-token':
#         return check_ftx_token_price()

#     elif coin == 'polkadot':
#         return check_polkadot_price()

#     elif coin == 'near':
#         return check_near_price()

#     elif coin == 'uniswap':
#         return check_uniswap_price()

#     elif coin == 'matic-network':
#         return check_polygon_price()

#     elif coin == 'cardano':
#         return check_ada_price()

#     elif coin == 'the-graph':
#         return check_the_graph_price()

#     elif coin == 'dogecoin':
#         return check_dogecoin_price()

