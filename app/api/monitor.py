from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.fyers_handler import fyers_auth

router = APIRouter(prefix="/monitor", tags=["monitor"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def monitor_page(request: Request):
    token = fyers_auth.load_access_token()
    
    if not token:
        return RedirectResponse(url="/?error=auth_required")
        
    user_profile = fyers_auth.get_user_profile(token)
    
    return templates.TemplateResponse("monitor.html", {
        "request": request,
        "user_profile": user_profile,
        "authenticated": True
    })
