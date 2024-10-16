# cloud-based-facial-recognition-access-system

# API Definition

- /unlock
- /user
  - /register
  - /update
  - /reservation
- /admin

# /unlock

ateway send data to the server, to validate if user has access

- method: POST
- request data:
  - embedding: list[float]
  - user_id?: int
  - lock_id: int
  - timestamp: float
- response data:
  - status: str
  - user_id?: int
  - embedding?: list[float]
  - session?:
    - user_id: int
    - lock_id: int
    - startAt: float
    - endAt: float

# /user

user interface

- method: GET
- response: HTML

# /user/register

user registration

- method: POST
- register user
- request data:
  - first_name
  - last_name
  - password
  - embedding: nparray

# POST /reservation/

room reservation

- method: POST
- request data:
  - user_id
  - lock_id
  - startAt
  - endAt
- response data:
  -
