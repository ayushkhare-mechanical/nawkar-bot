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
    """Handle manual token or URL submission"""
    from urllib.parse import urlparse, parse_qs
    
    form_data = await request.form()
    input_data = form_data.get("access_token", "").strip()
    
    if not input_data:
        raise HTTPException(status_code=400, detail="No data provided")
    
    try:
        access_token = None
        
        # Try to parse as URL
        if "://" in input_data or "?" in input_data:
            parsed_url = urlparse(input_data)
            params = parse_qs(parsed_url.query)
            
            # Check for access_token in URL
            if "access_token" in params:
                access_token = params["access_token"][0]
            # Check for auth_code in URL (in case SDK exchange is still possible/wanted)
            elif "auth_code" in params:
                auth_code = params["auth_code"][0]
                access_token = fyers_auth.generate_access_token(auth_code)
        
        # If no token extracted from URL, treat input as the raw token itself
        if not access_token:
            access_token = input_data

        # Save token
        fyers_auth.save_access_token(access_token)
        return RedirectResponse(url="/?status=success", status_code=303)
        
    except Exception as e:
        return RedirectResponse(url=f"/?status=error&message={str(e)}", status_code=303)
