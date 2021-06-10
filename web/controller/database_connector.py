import mysql.connector
import json
from mysql.connector import Error

class Database():

    def __init__(self):
        self.__host='db'
        self.__database='ecommerance'
        self.__password='manpro'
        self.__user='manpro'
        self.__port='3306'
        self.__auth_plugin='mysql_native_password'

    def __connect(self):
        self.__connection = mysql.connector.connect(host=self.__host,database=self.__database,user=self.__user,password=self.__password,port=self.__port,auth_plugin=self.__auth_plugin)
        self.__state = True

    def __close(self, connection):
        if self.__state :
            self.__connection.close()
        else :
            print("no connection")

    def __commit(self):
        self.__connection.commit()

    def run(self, query):
        try:
            self.__connect()
            cursor = self.__connection.cursor()
            cursor.execute(query)
            response = cursor.fetchall()
            self.__commit()
            self.__close(self.__connection)
        except Error as e:
            response = "Error while connecting to MySQL" + str(e)
        return json.dumps(response)

    def select(self,query):
        try:
            self.__connect()
            cursor = self.__connection.cursor()
            cursor.execute(query)
            response = cursor.fetchall()
            self.__close(self.__connection)
        except Error as e:
            response = "Error while connecting to MySQL" + str(e)
        return json.dumps(response)   

class ItemHandler():
    def __init__(self):
        self.conn = Database()

    def setitem(self,data):
        response = {
            'err_msg' : ""
        }
        ecommerce = 0
        if data['ecommerce'] == 'tokopedia':
            ecommerce = 2
        elif data['ecommerce'] == 'shopee':
            ecommerce = 1
        query = "SELECT id_barang FROM barang WHERE nama_barang = '{}'".format(data['name'])
        id_barang = json.loads(self.conn.select(query))
        #print(id_barang)
        if id_barang:
            #print('a')
            query = "UPDATE barang SET id_ecommerce = '{}', harga = '{}', harga_sebelum_diskon = '{}', diskon = '{}', rating = '{}', number_of_rating = '{}', nama_barang = '{}' WHERE id_barang = {}".format(ecommerce,data['price'],data['price_before_discount'],data['discount'],data['rating'],data['rating_count'],data['name'], id_barang[0][0])
        else:
            #print('b')
            query = "INSERT INTO barang (id_ecommerce, harga, harga_sebelum_diskon, diskon, rating, number_of_rating, nama_barang, gambar, link) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(ecommerce,data['price'],data['price_before_discount'],data['discount'],data['rating'],data['rating_count'],data['name'],data['image'],data['link'])
        self.conn.run(query)
        #print(query)
        return json.dumps(self.conn.select("SELECT * FROM barang WHERE nama_barang = '{}'".format(data['name']))), response

class HistoryHandler():
    def __init__(self):
        self.conn = Database()

    def sethistory(self,data):
        response = {
            'err_msg' : ""
        }
        data = json.loads(json.loads(data))
        query = "SELECT * FROM history WHERE id_barang = {}".format(data[0][0])
        dataold = json.loads(self.conn.select(query))
        print(dataold)
        if dataold:
            query = "UPDATE history SET total_search = '{}' WHERE id_history = '{}'".format(str(int(int(dataold[0][2])+int(1))),dataold[0][0])
        else:
            query = "INSERT INTO history (id_barang,total_search) VALUES ('{}', '1')".format(data[0][0])
        print(self.conn.run(query))
        return response

# dummy = {
#     "price" : 200000,
#     "price_before_discount": 110000,
#     "discount": 3,
#     "rating":5,
#     "rating_count":10,
#     "name": "Tokopedia Switch Nintendo",
#     "image": "www.tokopedia.com/gambar",
#     "link": "www.tokopedia.com/switch",
#     "ecommerce": "tokopedia"
# }
# data,response = ItemHandler().setitem(dummy)
# print(data)
# print(HistoryHandler().sethistory(data))
