from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
@router.post('/')
def post():
    return "post user"

 
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("user.html", {"request": request, "title": "Admin Panel", "message": "Hello, Admin!"})