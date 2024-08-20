import os
import motor.motor_asyncio


class MongoManager:
    __instance = None

    def __init__(self):
        print("Connect __init__.")

        if MongoManager.__instance != None:
            print("This class is a singleton")
            raise Exception("This class is a singleton!")
        else:
            print("call  getConnection")
            MongoManager.__instance = self.getConnection()

    @staticmethod
    def getInstance():
        print("Connect MongoDB.")
        if MongoManager.__instance == None:
            print("__instance == NONE")
            MongoManager()
        return MongoManager.__instance

    def getConnection(self):
        print("Connect getConnection")
        connURL = os.environ["DB_URL"]
        try:
            client = motor.motor_asyncio.AsyncIOMotorClient(connURL, serverSelectionTimeoutMS=5000)
            database = client["BetSoccerDB"]
            print(client.server_info())
            print("Connect SUCCESS.")
            return database
        except Exception:
            print("Unable to connect to the server.")
            return None
