import os
from binance.client import Client
import settings
import requests
import time
import sqlite3



bot_token = os.getenv('bot')
api_key = os.getenv('binance_api_key')
api_secret = os.getenv('binance_api_secret')

# Authenticate with the client
client = Client(api_key, api_secret)



# CONFIG
coin = 'BTC'
pairing = 'USDT'
period = 1 # dca period defined


# fn to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)


def get_info_coins_db():
    sqlite_connection = sqlite3.connect('customer.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    sqlite_select_query = """SELECT b_c.id_customer, b_c.name, b_c.coin, b_c.invested_money, b_c.amount_in_crypto, b_c.notified_or_not
        FROM BUY_COIN b_c"""
    cursor.execute(sqlite_select_query)
    user_info = cursor.fetchall()
    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
    cursor.close()
    return user_info


def buy_coin_btc():
    for i in range(len(get_info_coins_db())):
        return client.order_market_buy(
            symbol=coin+pairing,
            quantity = get_info_coins_db()[i][4]),


def main():
    while True:
        try:
            print("I AM BUYING BTC")
            buy_coin_btc()

        except Exception as e:
            print(e)
        # Каждую неделю покупаем
        time.sleep(604800)





# fancy way to activate the main() function
if __name__ == '__main__':
    main()
