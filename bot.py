import telebot
import sqlite3
import os
import settings
import crypto_price
import time


api_key = os.getenv('binance_api_key')
api_secret = os.getenv('binance_api_secret')
bot = telebot.TeleBot(os.getenv('bot'))


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
def buy_coin_bitcoin (message):
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



def create_record_into_db(message):
    if message.text == "/start":
        return start(message)
    userMoney = message.text
    userMoney = userMoney.lower()
    userMoney = userMoney.split()
    print(userMoney)
    crypto_coin = ['bitcoin', 'ethereum', 'binancecoin',
     'litecoin', 'solana', 'avalanche-2',
     'terra-luna', 'ftx-token',
     'polkadot', 'near', 'uniswap',
     'matic-network', 'cardano',
     'the-graph', 'dogecoin']
    try:
        coin, price = userMoney[0], userMoney[1]
        if userMoney[1].isdigit() or float(userMoney[1]) and userMoney[0] in crypto_coin:
            print('yes')
            price = float(price)
            user_money_in_btc = 1 * price / crypto_price.check_btc_price()
            user_money_in_btc = round(user_money_in_btc, 5)
            bot.send_message(message.chat.id, f'Your {price}$ in {coin[0].upper() + coin[1::]} is {user_money_in_btc}₿.')
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
                                                "\nBitcoin 50.")
        bot.register_next_step_handler(msg, buy_coin_bitcoin_on_user_money)

bot.polling(none_stop=True, timeout=123)