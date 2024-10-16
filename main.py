from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse 
import uvicorn  
from routes.unlock import router as unlock_router
from routes.admin import router as admin_router
from routes.user import router as user_router
 

app = FastAPI()  
app.include_router(unlock_router, prefix='/unlock')
app.include_router(admin_router, prefix='/admin')
app.include_router(user_router, prefix='/user')

templates = Jinja2Templates(directory="templates") 

# @app.get('/', response_class=HTMLResponse)
# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get('/admin', response_class=HTMLResponse)
# async def admin(request: Request):
#     return templates.TemplateResponse("admin.html", {"request": request})

# @app.get('/user', response_class=HTMLResponse)
# async def user(request: Request):
#     return templates.TemplateResponse("user.html", {"request": request})


# @app.post('/register/')
# async def facial_register(request: Request):
#     received_data = await request.g
#     unknown_encoding = pickle.load(received_data)
#     users.append(unknown_encoding)


if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=8013)