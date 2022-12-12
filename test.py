from main import DataClient
from database import BotDatabase

db = BotDatabase()
client = DataClient(db)


list_ = client.genshin.get_characters()

list_[0].fetch()

print(list_[0].data)