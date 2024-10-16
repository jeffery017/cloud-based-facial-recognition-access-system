from fastapi import FastAPI 
import uvicorn  
from routes.unlock import router as unlock_router
from routes.admin import router as admin_router
from routes.user import router as user_router
from routes.index import router as index_router

app = FastAPI()  
app.include_router(index_router)
app.include_router(unlock_router, prefix='/unlock')
app.include_router(admin_router, prefix='/admin')
app.include_router(user_router, prefix='/user')

if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=8000)