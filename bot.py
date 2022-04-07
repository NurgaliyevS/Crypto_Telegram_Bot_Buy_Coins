import telebot
import sqlite3
import os
import settings
import crypto_price
import time
import pandas as pd
from pycoingecko import CoinGeckoAPI

api_key = os.getenv('binance_api_key')
api_secret = os.getenv('binance_api_secret')
bot = telebot.TeleBot(os.getenv('bot'))
cg = CoinGeckoAPI()

def create_db_for_buy_coin():
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS BUY_COIN (
                        id_customer INTEGER,
                        name VARCHAR (40),
                        coin VARCHAR (50),
                        invested_money INTEGER,        
                        amount_in_crypto INTEGER,
                        notified_or_not INTEGER NOT NULL CHECK(notified_or_not in (0,1))
                        )""")
    connect.commit()

@bot.message_handler(commands=['buy'])
def buy_coin (message):
    msg = bot.send_message(message.chat.id, "I can buy only Bitcoin."
                                            "\nCount everything in dollars."
                                              "\n"
                                              "\nExample: "
                                              "\nBitcoin 50"
                                                    "\n"
                                            "\nThis means that"
                                                    "\nI will buy $50 worth of bitcoins. "
                                                    "\n"
                                                    "\nIf you want to exit?"
                                                    "\n/start")
    bot.register_next_step_handler(msg, create_record_into_db)

#### ЧТЕНИЕ ВСЕГО ЧТО ЕСТЬ В БАЗЕ ДАННЫХ
#### НЕОБХОДИМО БРАТЬ ОБРАБОТАТЬ ЭТИ ДАННЫЕ
@bot.message_handler(commands=['record'])
def read_sqlite_table(message):
    try:
        bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
        # time.sleep(10)
        sqlite_connection = sqlite3.connect('customer.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_select_query = """SELECT b_c.name, b_c.coin, b_c.invested_money, b_c.amount_in_crypto
            FROM BUY_COIN b_c"""
        cursor.execute(sqlite_select_query)
        text = cursor.fetchall()
        print("Всего строк: ", len(text))
        # print("Вывод каждой строки")
        a = []
        #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
        #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
        #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
        for rows in text:
            a.append(rows)
        c = list()
        for i in range(len(a)):
            c.append(a[i])
        c = str(c)
        c = c.replace('(', '\n', 1).replace('[', ' ').replace('(', '\n').replace(')','').replace(']', ' ').replace("'",'')
        print(c)
        cursor.close()
        bot.send_message(message.chat.id, f'{c}')
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def list_coins():
    # bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
    sqlite_connection = sqlite3.connect('coins.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    sqlite_select_query = f"""SELECT cm.id
    FROM Coins_Markets cm"""
    cursor.execute(sqlite_select_query)
    text = cursor.fetchall()
    cursor.close()
    text = str(text)
    result = text.replace("[", "").replace("(", "").replace("'","").replace(",","").replace(")","\n").replace("]","")
    return result

def create_record_into_db(message):
    if message.text == "/start":
        return (message)
    userMoney = message.text
    userMoney = userMoney.lower()
    userMoney = userMoney.split()
    if userMoney[0] in list_coins():
        print('yes')
    try:
        coin, price = userMoney[0], userMoney[1]
        if userMoney[1].isdigit() or float(userMoney[1]) and userMoney[0] in list_coins():
            print('yes')
            price = float(price)
            user_money_in_btc = 1 * price / crypto_price.check_crypto_price(coin)
            print(user_money_in_btc)
            user_money_in_btc = round(user_money_in_btc, 5)
            bot.send_message(message.chat.id, f'Your {price}$ in {coin[0].upper() + coin[1::]} is {user_money_in_btc}.')
            connect = sqlite3.connect('customer.db')
            cursor = connect.cursor()
            cursor.execute("INSERT INTO BUY_COIN (id_customer, name, coin, invested_money, amount_in_crypto , notified_or_not) VALUES (? ,?, ?, ?, ?, ?);", (message.chat.id, message.from_user.first_name, coin, price, user_money_in_btc,0))
            connect.commit()
            cursor.close
            connect.close()
            return user_money_in_btc
    except:
        msg = bot.send_message(message.chat.id, "I don't get it."
                                                "\nTry again, please."
                                                "\nExample:"
                                                "\nBitcoin 50")
        bot.register_next_step_handler(msg, buy_coin)

def find_crypto(message):
    try:
        crypto_price.get_top_100_coins()
        user_coin = message.text
        user_coin = user_coin.lower()
        # coin_plot(user_coin.user_coin)
        print(user_coin)
        sqlite_connection = sqlite3.connect('coins.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        cursor.execute("SELECT cm.market_cap_rank,cm.id, cm.name, cm.current_price, cm.price_change_24h, cm.price_change_percentage_24h, cm.market_cap, cm.market_cap_change_percentage_24h,cm.total_volume, cm.circulating_supply, cm.max_supply, cm.high_24h, cm.low_24h FROM Coins_Markets cm WHERE cm.id = ?", (user_coin,))
        data = cursor.fetchone()
        user = []
        print(data)
        print('hey', data[10])
        for i in data:
            user.append(i)
        if user[10] is None:
            user[10] = 0
        sqlite_connection.commit()
        cursor.close()
        result = 'Market Cap Rank: {} \nName: {} \nPrice: {}$ \nPrice Change 24h: {}$ \nPrice Change 24h: {}% \nMarket Cap: {:,} \nMarket Cap 24h: {}% \nTotal Volume: {:,} \nCirculating Supply: {:,} \nMax suply: {:,} \nLow Price 24h: {}$ \nHigh price 24h: {}$'.format(user[0], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10], user[12], user[11])
        bot.send_message(message.chat.id, result)
    except:
        bot.send_message(message.chat.id, "I can't find crypto with this name"
        "\nCheck this file"
        "\n/list_coins"
        "\nCorrect names of coins"
        "\nThen, try again"
        "\n/find")

bot.polling(none_stop=True, timeout=123)