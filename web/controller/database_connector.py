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

# def run():
#     try:
#         connection = mysql.connector.connect(host='db', database='ecommerance', user='manpro', password='manpro', port='3306', auth_plugin= 'mysql_native_password')
#         response = 'success'
#         connection.close()
#     except Error as e:
#         response = "Error while connecting to MySQL" + str(e)
#     return response