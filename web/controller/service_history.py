import database_connector

class ServiceHistory():
    def __init__(self):
        db = database_connector.Database()
    
    def updatehistory(self,idbarang,idecommerce):
        print()