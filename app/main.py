from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api import auth
import os

app = FastAPI(title="Nawkar Trading Bot")

# Mount templates
templates = Jinja2Templates(directory="app/templates")

# Include routes
app.include_router(auth.router)

@app.api_route("/", methods=["GET", "HEAD"])
async def index(request: Request):
    # Check if we have a saved token
    from app.core.fyers_handler import fyers_auth
    token = fyers_auth.load_access_token()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "authenticated": token is not None,
        "token_preview": f"{token[:10]}..." if token else None
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
