from fastapi import APIRouter
from fastapi import BackgroundTasks
from pydantic import BaseModel
import numpy as np
from numpy.typing import NDArray
from typing import Optional
from libs.db import Model
from qdrant_client import models

debug = 0


from libs.FacialRecognition import validate_user  , getUsers
valid_users = getUsers() 

class SessionData(BaseModel):
    user_id: int
    lock_id: int
    startAt: float
    endAt: float

class LogData(BaseModel):
    user_id: int
    lock_id: int
    timestamp: float
    embedding: list
    result: str

class RequestData(BaseModel):
    user_id: Optional[int] = 0
    lock_id: int
    timestamp: float
    embedding: list

class ResponseData(BaseModel):
    status: str
    user_id: Optional[int]
    embedding: Optional[list]
    session: Optional[SessionData]


router = APIRouter()
@router.post('/')
async def unlock(data: RequestData, background_tasks: BackgroundTasks):
    print(valid_users)
    logd(f'data: {data}')
    # parse request data
    embedding = np.array(data.embedding)
    if data.user_id:
        user_id = data.user_id
    lock_id = data.lock_id 
    logd(f'user_id: {user_id}')
    logd(f'lock_id: {lock_id}')
    # if request without user_id, search user_id by embedding in database -> user_id
    if (not user_id):
        user_id = getUserIdByEmbedding(embedding)


    # search session by user_id in database -> matched session
    if (user_id):
        session = getSession(user_id, lock_id)

    # log unlock request
    background_tasks.add_task(func=logUnlockRequest, data=data)

    # return response to the client (gateway)
    response = getResponse(user_id=user_id, embedding=embedding, session=session)
    logd(response)
    return response




def checkEmbeddingType(embedding):
    return True

def getUserIdByEmbedding(embedding: NDArray)-> int:
    logd("Get user_id by embedding.")
    client = Model.getClient()

    search_result = client.search(
        collection_name='RegisteredUsers',
        query_vector=np.array(np.array(embedding)),
        limit=1  # We only need the closest match
    )

    if validate_user(valid_users, embedding):
        logd("user_id not found")
    return search_result[0].payload['uuid']


def getSession(user_id: int, lock_id: int)->int:
    logd("Get session by user_id.")
    #search through reservations for specified user id and lock id and return information
    client = Model.getClient()
    response = client.query_points(
        collection_name="Reservations",
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="uuid",
                    match=models.MatchValue(
                        value=user_id
                    )
                ),
                models.FieldCondition(
                    key="lock_id",
                    match=models.MatchValue(
                        value=lock_id
                    )
                )

            ]
        )
    )


    for point in response.points:
        uuid = point.payload.get("uuid")
        lock_id = point.payload.get("lock_id")
        start_At = point.payload.get("startAt")
        end_At = point.payload.get("endAt")

    #verify attributes if needed (response userid and lockid must be matching with given parameters)

    return SessionData(
        user_id=point.payload.get("uuid"),
        lock_id=point.payload.get("lock_id"),
        startAt=point.payload.get("start_At"),
        endAt=point.payload.get("end_At")
    )

def logUnlockRequest(data: LogData)->None: 
    logd("Log the unlock request.") 

def getResponse(user_id:int, embedding:list[float], session=SessionData)->ResponseData:
    logd("Get response data.")
    return ResponseData(user_id=user_id, embedding=embedding, session=session)
    
def logd(message):
    if debug:
        print(message)

