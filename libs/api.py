from db import Model
from qdrant_client.models import PointStruct
client = Model.getClient()

def getReservedSession(lock_id, date):
    client.scroll(
        collection_name='Reservations'
    )
    #use filter for 'lock_id' matching lock_id arg
    # search all reservation with lock_id
    # session.endAt > today
    # today + 14days > session.endAt

    # return list[Session]



def insertSession(user_id, lock_id, startAt, endAt):
    #may need to pass client as a parameter for this function and not import
    client.upsert(
        collection_name='Reservations',
        points=[
            PointStruct(
                id=user_id,
                payload={
                    "uuid": user_id,
                    "lock_id": lock_id,
                    "startAt": startAt,
                    "endAt": endAt,
                }
            )
        ]
    )


def userLogin(name, password):
    # search by user and password
    return True

