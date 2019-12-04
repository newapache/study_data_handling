from socket import *
import time
import configparser
import sqlite3
import sys

cryp_list = ['BTC','ETH']
trgt_list = ['USD','JPY','EUR','KRW']
table = ''


def get_configuration(configFile):
    config = configparser.RawConfigParser()
    config.read(configFile)
    return config


def get_db_configuration(configFile, section='DB_DEFAULT'):
    c = get_configuration(configFile)
    return c[section]


def get_web_configuration(configFile, section='WEBSERVER_DEFAULT'):
    c = get_configuration(configFile)
    return c[section]


def get_connection(configProps):
    try:
        conn = sqlite3.connect(configProps['DB.db'])
        return conn
    finally:
        pass


def get_data(conn, cryp_curr, trgt_curr):

    cursor = conn.cursor()
    cursor.execute("select CurrentTime, Price from %s where cryptocurrencyname = ? and targetcurrencyname = ?" % table, (cryp_curr.upper(), trgt_curr.upper()))
    return cursor.fetchall()


if __name__ == "__main__":
    config = sys.argv[1]
    db_c = get_db_configuration(config)
    c = get_web_configuration(config)
    PORT = int(c['web.port'])
    BUFSIZE = int(c['web.bufsize'])
    table = db_c['DB.db']
    listen_sock = socket(AF_INET, SOCK_STREAM)
    listen_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listen_sock.bind(('', PORT))
    listen_sock.listen(2)

    while 1:
        conn, addr = listen_sock.accept()
        data = conn.recv(BUFSIZE).decode("ascii")
        recv_arr = data.replace(' ','/').split('/')
        cryp_curr = recv_arr[2]
        trgt_curr = recv_arr[3]

        if cryp_curr.upper() in cryp_list and trgt_curr.upper() in trgt_list:
            db_conn = get_connection(db_c)
            price_data = get_data(db_conn, cryp_curr, trgt_curr)
            price_str = ''
            for item in price_data:
                today = time.strftime("%Y-%m-%d", time.localtime())
                if today == item[0].split(' ')[0]:
                    price_str += item[0] + "&nbsp; &nbsp;" + str(item[1]) + "<br/>"

            msg = """HTTP/1.1 200 OK

            <html><body><h1>price Table:</h1> %s </body></html>""" % price_str

            conn.sendall(msg.encode('utf-8'))
            conn.close()
