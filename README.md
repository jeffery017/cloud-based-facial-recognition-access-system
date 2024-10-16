# cloud-based-facial-recognition-access-system

# API Define

- /unlock
- /user
  - /register
  - /update
  - /reservation
- /admin

# POST /unlock/

ateway send data to the server, to validate if user has access

request:

- embedding: list[float]
- user_id: int
- lock_id: int
- timestamp: float

response:

- user_id: int
- embedding: list[float]
- session:
  - user_id: int
  - lock_id: int
  - startAt: float
  - endAt: float

# POST /user/register/

register user
data:

- first_name
- last_name
- password
- embedding: nparray

POST /user

POST /reservation/
