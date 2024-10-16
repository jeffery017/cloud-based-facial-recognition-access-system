from fastapi import APIRouter
from fastapi import BackgroundTasks
from pydantic import BaseModel
import numpy as np
from numpy.typing import NDArray

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
    user_id: int
    lock_id: int
    timestamp: float
    embedding: list

class ResponseData(BaseModel):
    user_id: int
    embedding: list
    session: SessionData


router = APIRouter()
@router.post('/')
async def unlock(data: RequestData, background_tasks: BackgroundTasks):
    print(valid_users)
    logd(f'data: {data}')
    # parse request data
    embedding = np.array(data.embedding)
    
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



def getUserIdByEmbedding(embedding: NDArray)-> int:
    logd("Get user_id by embedding.")
    if validate_user(valid_users, embedding):
        logd("user_id not found")
    return 1 

def getSession(user_id: int, lock_id: int)->int:
    logd("Get session by user_id.")
    return SessionData(
        user_id=1, 
        lock_id=1, 
        startAt=1729039060.210011, 
        endAt=1729040060.210011)

def logUnlockRequest(data: LogData)->None: 
    logd("Log the unlock request.") 

def getResponse(user_id:int, embedding:list[float], session=SessionData)->ResponseData:
    logd("Get response data.")
    return ResponseData(user_id=user_id, embedding=embedding, session=session)
    
def logd(message):
    if debug:
        print(message)

