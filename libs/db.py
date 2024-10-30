
from qdrant_client import QdrantClient 
import os
from dotenv import load_dotenv
ak = os.getenv("QDRANT_API_KEY")
end = os.getenv("QDRANT_ENDPOINT")
 

class Model:
    __client =  QdrantClient(
        url=end,
        api_key=ak
    )

    @staticmethod
    def getClient():
        return Model.__client
 


