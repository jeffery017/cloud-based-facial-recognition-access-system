
import os
from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams 
from dotenv import load_dotenv

class Model:
    __client =  QdrantClient(
        url=os.getenv("QDRANT_ENDPOINT"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    @staticmethod
    def getClient():
        return Model.__client
 

client = Model.getClient()
#delete user registry collection on start up (fresh database on launch)
client.delete_collection(collection_name='RegisteredUsers')
#create user registry collection
client.create_collection(
    collection_name='RegisteredUsers',
    vectors_config=VectorParams(size=4, distance=Distance.DOT)
)


