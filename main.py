from database import BotDatabase
from datetime import datetime
from requests_cache import CachedSession
from utils import generate_id

class DataClient:

    def __init__(self, database: BotDatabase) -> None:

        self.mongodbclient = database
        self.db = self.mongodbclient.data
        self.check_interval = {
            'characters' : 86400 * 30 #after a month
        }
        self._session = CachedSession(
                            cache_name='data.client',
                            backend='mongodb',
                            expire_after=7200,
                            serializer='pickle',
                            allowable_methods='GET',
                            stale_if_error=True
        )



    def game_exists(self, game_name: str):

        checker = self.db.list_collection_names(filter={'name': game_name})
        return len(checker) != 0
    

    def data_id(self, game_name: str, data_id : str, **kwargs):

        kwargs.setdefault({''})

        if self.game_exists(game_name):
            filters = {'data_id': data_id}, {'_id': 1}
            filters = {**filters, **kwargs}
            checker = list(self.db.get_collection(game_name).find(filters))
            return checker 
    
    def save_data(self,  game_name: str, data_id : str,  data : dict):

        
        data_checker = self.data_id(game_name, data_id)

        if bool(data_checker):       
            id_ = data_checker[0]['_id']
            collection = self.mongodbclient.collection('data', game_name)

            collection.update_one({'_id': id_}, {'$set': {**{'type': data['type'], 'data_id': generate_id(data['name']), 'timestamp': datetime.now().strftime('%c')}, **data}})

        else:
            
            collection = self.mongodbclient.collection('data', game_name)
            collection.insert_one({**{'type': data['type'], 'data_id': generate_id(data['name']), 'timestamp': datetime.now().strftime('%c')}, **data})
    
    def get_data(self, game_name: str, data_id : str):
        
        data_checker = self.data_id(game_name, data_id)
        
        if bool(data_checker):   
            data_ = data_checker[0].copy()
            data_.pop('_id')
            return data_
        
        
            
    
    def pending_update(self, game_name: str, data_id : str):

        data_checker = self.data_id(game_name, data_id)

        if bool(data_checker):    

            timestamp_last = datetime.strptime(data_checker['timestamp'], '%c')

            return (self.timestamp - timestamp_last).total_seconds() > self.check_interval[data_checker['type']]
        
        else:

            return True

