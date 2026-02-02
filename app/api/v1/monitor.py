from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.fyers_handler import fyers_auth

router = APIRouter(prefix="/monitor", tags=["monitor"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/data")
async def get_monitor_data():
    token = fyers_auth.load_access_token()
    
    if not token:
        return {"authenticated": False, "message": "Authentication required"}
        
    user_profile = fyers_auth.get_user_profile(token)
    
    return {
        "authenticated": True,
        "user_profile": user_profile,
        "features": [
            {"name": "Fyers Connectivity", "status": "Active", "icon": "zap"},
            {"name": "Profile Management", "status": "Active", "icon": "user"},
            {"name": "Token Automation", "status": "Active", "icon": "lock"}
        ]
    }
