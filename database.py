from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import *
import json
from string import punctuation
from datetime import  datetime

#self.client

#self.client.name ----> database name
#self.client.database.name ----> collection name
#self.client.data.name.[documents] ---> document




class BotDatabase:

    def __init__(self) -> None:

        self.client = MongoClient('mongodb://127.0.0.1/', port=27017)
        self.data : Database = self.client.data
  

    def collection(self, database_name: str, item_id : str) -> Collection:
       
        filter = {"name": item_id}
        checker = self.client[database_name].list_collection_names(filter=filter)
        print(filter)
        if len(checker) != 0:
            return self.client[database_name][item_id]
        else:
            return self.client[database_name].create_collection(item_id)

    def document(self, database_name : str, item_id : str, return_id : bool = False) -> dict:

        filter = {"name": item_id}
        checker = self.client[database_name].list_collection_names(filter=filter)        
        if len(checker) != 0:
            dict__ = {}
            id_filter = 1 if return_id else 0            
            for doc in self.client[database_name][item_id].find({}, {'_id': id_filter}):
                
                dict__ = {**dict__, **doc}
            
            return dict__
        
        return None
        
    
    @property
    def timestamp(self):
        return datetime.now()


    def update(self, database_name: str, item_id: str, updated_data: dict) -> bool:

        filter = {"name": item_id}
        checker = self.client[database_name].list_collection_names(filter=filter)        
        if len(checker) != 0:
            dict__ = {}
            id_filter = 1     
            if len(list(self.client[database_name][item_id].find({}, {'_id': id_filter}))) != 0: 
                id_ = list(self.client[database_name][item_id].find({}, {'_id': id_filter}))[0]['_id']
                self.client[database_name][item_id].update_one({'_id': id_}, {'$set': updated_data})
            else:
                self.client[database_name][item_id].insert_one(updated_data)


            
            return True
             
        return False


'''
test = BotDatabase()
data = test.collection('data', 'genshin')
data.insert_one({**{'type': 'characters', 'data_id': generate_id('albedo'), 'timestamp': datetime.now().strftime('%c')}, **data_})

'''