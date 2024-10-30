import datetime
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
@router.post('/')
def post():
    return "post user"

 
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})




@router.get("/reservation",  response_class=HTMLResponse)
async def reservation(request:Request):
    today = datetime.now()
    dates = [(today + datetime.timedelta(days=i)).strftime("%Y/%m/%d") for i in range(14)]
    available_sessions = list(range(24))
    return templates.TemplateResponse("reservation.html", 
    {
        "request": request, 
        "dates": dates, 
        "sessions": available_sessions
    })