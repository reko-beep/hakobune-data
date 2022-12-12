from main import DataClient
from database import BotDatabase

db = BotDatabase()
client = DataClient(db)


list_ = client.genshin.get_characters()


list_[2].fetch(True)

print(list_[2].data)