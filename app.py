from fastapi import FastAPI 
import uvicorn  
from routes.unlock import router as unlock_router
from routes.admin import router as admin_router
from routes.user import router as user_router
from routes.index import router as index_router
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from uuid import uuid4
import numpy as np
import os
import dotenv as load_dotenv

load_dotenv()

app = FastAPI()  
app.include_router(index_router)
app.include_router(unlock_router, prefix='/unlock')
app.include_router(admin_router, prefix='/admin')
app.include_router(user_router, prefix='/user')

if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=8000)
    ak = os.getenv("QDRANT_API_KEY")
    end = os.getenv("QDRANT_ENDPOINT")

    client = QdrantClient(
        url=end,
        api_key=ak
    )

    #delete user registry collection on start up (fresh database on launch)
    client.delete_collection(collection_name='RegisteredUsers')
    #create user registry collection
    client.create_collection(
        collection_name='RegisteredUsers',
        vectors_config=VectorParams(size=4, distance=Distance.DOT)
    )


