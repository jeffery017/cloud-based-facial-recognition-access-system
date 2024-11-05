#THE FOLLOWING CODE SHOULD BE RUN ONCE ON INITIALIZATION

import os
from uuid import uuid4
import face_recognition
import numpy as np
from numpy._typing import NDArray
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams 
from dotenv import load_dotenv, find_dotenv
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import Filter, SearchRequest
import numpy
from pathlib import Path


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
    vectors_config=VectorParams(size=128, distance=Distance.DOT)
)

#create table for lockid (just uuid for locks/potential room reservations)
client.create_collection(
    collection_name='LockIDs',
    vectors_config=VectorParams(size=128,distance=Distance.DOT)
)

client.create_collection(
    collection_name="Reservations",
    vectors_config=VectorParams(size=128, distance=Distance.DOT)
)


#------------------------------------------------------------ TEST CODE IGNORE ------------------------------------------------------------------------
class User:
    firstName: str
    lastName: str
    encoding: NDArray

    def __init__(self, firstName: str, lastName: str, encoding: NDArray):
        self.firstName = firstName
        self.lastName = lastName
        self.encoding = encoding

    def __str__(self) -> str:
        return f"User(firstName: {self.firstName}, lastName: {self.lastName})"


def facialEncoding(file_path):
    try:
        user_image = face_recognition.load_image_file(file_path)
        user_encoding = face_recognition.face_encodings(user_image)[0]
        return user_encoding
    except:
        return None


# get the sub directories
def getSubdirs(directory):
    if os.path.isdir(directory):
        return [d.name for d in directory.iterdir() if d.is_dir()]
    print(f"Not a directory: {directory}")
    return []


# parse user's data from the dataset (firstname, lastname, encode)
def parseDateFromDirectory(dName):
    # get image path
    path = os.path.join(directory, f"{dName}/{dName}_0001.jpg")
    # check if image exists
    if os.path.isfile(path):
        encode = facialEncoding(path)
        if encode is not None and encode.any():
            # parse data and transfer to python class
            firstName, lastName = dName.split("_")
            uid = str(uuid4())
            lid = str(uuid4())
            client.upsert(
                collection_name='RegisteredUsers',
                points=[
                    PointStruct(
                        id=uid,
                        vector=encode.tolist(),
                        payload={
                            "first_name": firstName,
                            "last_name": lastName,
                            "uuid": uid,
                            "encoding": encode.tolist()  # np.array(encode) to return back to numpy array
                        }
                    )
                ]
            )
            return {"first_name": firstName, "last_name": lastName, "uuid": uid, "encoding": encode.tolist()}
    return None


def getStoredData():
    scroll_result, next_page = client.scroll(
        collection_name='RegisteredUsers',
        limit=100  # Adjust the limit as needed
    )

    # Extract and print full names
    for point in scroll_result:
        payload = point.payload
        full_name = f"{payload['first_name']} {payload['last_name']} Encoding: {payload['encoding'][0]}"
        print(full_name)


# Demo code for getting data
if __name__ == "__main__":
    client = QdrantClient(
        url=os.getenv('QDRANT_ENDPOINT'),
        api_key=os.getenv('QDRANT_API_KEY')
    )
    directory = Path('/Users/OQUENDI/Downloads/lfw_funneled')
    limit = 10
    subdirs = getSubdirs(directory)
    for i in range(limit):
        inserted_data = parseDateFromDirectory(subdirs[i])
        if inserted_data:
            print(f"Inserted data: {inserted_data}")
    getStoredData()