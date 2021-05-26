import database_connector
import json

class ServiceHistory():
    def __init__(self):
        self.db = database_connector.Database()
    
    def updatehistory(self,idecommerce,idbarang):
        query = 'SELECT id_history FROM history WHERE id_barang = "'+str(idbarang)+'" AND id_ecommerce = "'+ str(idecommerce) +'"'
        response = json.loads(self.db.select(query))
        if len(response) == 0:
            query = 'SELECT COUNT(*) FROM history'
            idhistory = json.loads(self.db.select(query))[0][0]
            idhistory = int(idhistory) + 1
        else:
            idhistory = response[0][0]
        query = 'SELECT total_search FROM history WHERE id_barang = "'+str(idbarang)+'" AND id_ecommerce = "'+ str(idecommerce) +'"'
        response = json.loads(self.db.select(query))
        if len(response) == 0:
            totalsearch = 1
            query = 'INSERT into history VALUES ("'+ str(idhistory) +'", '+ str(idecommerce) +', ' + str(idbarang) + ', '+ str(totalsearch) +')'
            self.db.run(query)
        else:
            totalsearch = int(response[0][0]) + 1
            query = 'UPDATE history SET total_search="'+str(totalsearch)+'" WHERE id_history="'+str(idhistory)+'"'
            self.db.run(query)
        # print(totalsearch)
        return idhistory
        # print(idhistory)
        # print(totalsearch)

# test = ServiceHistory()
# print(test.updatehistory(1,343))