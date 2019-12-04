import urllib.request
import os, ssl
import threading
import json
import configparser
import configuration
import sqlite3
import sys
import time


database = ''
table = ''

def get_configuration(configFile):
    config = configparser.RawConfigParser()
    config.read(configFile)
    return config


def get_db_configuration(configFile, section='DB_DEFAULT'):
    c = get_configuration(configFile)
    return c[section]


def create_db(tb):
    con = sqlite3.connect(database)
    cursor = con.cursor()

    cursor.execute("drop table if exists %s" % table)
    cursor.execute("""create table %s (
            CurrentTime varchar(20) not null,
            CryptoCurrencyName varchar(10) not null,
            TargetCurrencyName varchar(10) not null,
            Price decimal(20,5) not null
            ); """ % table)
    con.commit()
    cursor.close()
    con.close()


def request(url):
    curr = url.rsplit('&')[0][-3:]
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        res = urllib.request.urlopen(req)
        price_data = res.read().decode('utf-8')
    except Exception as e:
        print(str(e))

    insert_db(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), curr, price_data)

    # every 10 minutes
    timer = threading.Timer(600, request, [url])
    timer.start()


def insert_db(time, curr, price_data):
    price_dict = json.loads(price_data)
    con = sqlite3.connect(database)
    cursor = con.cursor()

    for k,v in price_dict.items():
        cursor.execute("insert into %s values(?,?,?,?)" % table, (time, curr, k, v))

    con.commit()
    cursor.close()
    con.close()


if __name__ == "__main__":
    #get config data
    config = sys.argv[1]
    c = get_db_configuration(config)
    database = c['db.db']
    table = c['db.db']

    #create database
    create_db(table)

    # get btc,eth data  &  insert database
    thread1 = threading.Thread(target = request, args = ('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR,KRW',))
    thread1.start()
    thread2 = threading.Thread(target = request, args = ('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,JPY,EUR,KRW',))
    thread2.start()
