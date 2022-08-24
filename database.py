import pymongo
from config import *


class Database:

    def __init__(self):
        client = pymongo.MongoClient(URL_DB)
        self.db = client.services
        self.channels = self.db.channels

    
    def get_channel_launch(self):
        try:
            channel = self.channels.find_one({"launch": True})
            return channel
        except Exception as error:
            logger.error(error)
            return 0

    
    def suspend_channel(self, id):
        try:
            self.channels.update_one({"_id": id}, {"$set": {"launch": False}})
            return 1
        except Exception as error:
            logger.error(error)
            return 0