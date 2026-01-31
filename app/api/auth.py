from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.core.fyers_handler import fyers_auth

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/login")
async def login():
    """Redirect to Fyers login page"""
    login_url = fyers_auth.get_login_url()
    return RedirectResponse(url=login_url)

@router.get("/callback")
async def callback(request: Request):
    """Handle OAuth callback from Fyers"""
    auth_code = request.query_params.get("auth_code")
    if not auth_code:
        raise HTTPException(status_code=400, detail="Authorization code not found in request")
    
    try:
        # Generate and save token
        access_token = fyers_auth.generate_access_token(auth_code)
        fyers_auth.save_access_token(access_token)
        
        # Redirect back to home with success
        return RedirectResponse(url="/?status=success")
    except Exception as e:
        return RedirectResponse(url=f"/?status=error&message={str(e)}")
