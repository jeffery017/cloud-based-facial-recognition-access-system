
import os
from uuid import uuid4

import numpy as np
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams 
from dotenv import load_dotenv, find_dotenv
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import Filter, SearchRequest
import numpy


load_dotenv()
class Model:
    __client =  QdrantClient(
        url=os.getenv('QDRANT_ENDPOINT'),
        api_key=os.getenv('QDRANT_API_KEY')
    )

    @staticmethod
    def getClient():
        return Model.__client
 

client = Model.getClient()
#delete user registry collection on start up (fresh database on launch)
client.delete_collection(collection_name='RegisteredUsers')
client.delete_collection(collection_name='LockIDs')
client.delete_collection(collection_name='Reservations')

#create user registry collection: first name, last name, user_id, embedding
client.create_collection(
    collection_name='RegisteredUsers',
    vectors_config=VectorParams(size=4, distance=Distance.DOT)
)

#create table for lockid (just uuid for locks/potential room reservations)
client.create_collection(
    collection_name='LockIDs',
    vectors_config=VectorParams(size=1,distance=Distance.DOT)
)

client.create_collection(
    collection_name="Reservations",
    vectors_config=VectorParams(size=4, distance=Distance.DOT)
)

uuid_to_search = str(uuid4())
lock_id_to_search = str(uuid4())

def insertTest():
    #insert single individual test
    client.upsert(
                collection_name='RegisteredUsers',
                points=[
                    PointStruct(
                        id=uuid_to_search,
                        vector=[0.1,0.2,0.3,0.4], #randomize this
                        payload={
                            "first_name": "Bob",
                            "last_name": "Dylan",
                            "uuid": uuid_to_search,
                            "lock_id":lock_id_to_search,
                            "encoding": [0.1,0.4],
                        }
                    )
                ]
            )
def findNearestReturnPoints(target_encoding):
    qresp = client.query_points(
        collection_name='RegisteredUsers',
        query=np.array(target_encoding),  # <--- Dense vector
    )
    return qresp

insertTest()
response = client.query_points(
    collection_name="RegisteredUsers",
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="uuid",
                match=models.MatchValue(
                    value=uuid_to_search
                )
            ),
            models.FieldCondition(
                key="lock_id",
                match=models.MatchValue(
                    value=lock_id_to_search
                )
            )

