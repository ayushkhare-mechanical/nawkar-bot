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

@router.post("/manual")
async def manual_token(request: Request):
    """Handle manual token submission via JSON"""
    try:
        data = await request.json()
        input_data = data.get("access_token", "").strip()
        
        if not input_data:
            return {"success": False, "message": "No data provided"}
        
        access_token = None
        
        # Try to parse as URL
        from urllib.parse import urlparse, parse_qs
        if "://" in input_data or "?" in input_data:
            parsed_url = urlparse(input_data)
            params = parse_qs(parsed_url.query)
            
            if "access_token" in params:
                access_token = params["access_token"][0]
            elif "auth_code" in params:
                auth_code = params["auth_code"][0]
                access_token = fyers_auth.generate_access_token(auth_code)
        
        if not access_token:
            access_token = input_data

        if not fyers_auth.validate_token(access_token):
            return {"success": False, "message": "Invalid or Expired Fyers Token"}

        fyers_auth.save_access_token(access_token)
        return {"success": True, "message": "Token saved successfully"}
        
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.get("/logout")
async def logout():
    """Clear the Fyers session"""
    fyers_auth.logout()
    return {"success": True, "message": "Logged out successfully"}

@router.get("/status")
async def auth_status():
    """Check if authenticated"""
    token = fyers_auth.load_access_token()
    return {"authenticated": token is not None}
