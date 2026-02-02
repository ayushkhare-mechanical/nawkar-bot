from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api import auth
import os

app = FastAPI(title="Nawkar Trading Bot")

# Setup CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for dev: localhost:5173, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount templates
templates = Jinja2Templates(directory="app/templates")

# Include routes
from app.api.v1 import router as api_v1_router
app.include_router(api_v1_router)

# Serve React App (Production)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Check if frontend build exists
frontend_dist = os.path.join(os.getcwd(), "frontend", "dist")

if os.path.exists(frontend_dist):
    # Mount static assets
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    # Catch-all route for SPA
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow API calls to pass through
        if full_path.startswith("api") or full_path.startswith("auth"):
            return None # 404 handled by API router
            
        response = FileResponse(os.path.join(frontend_dist, "index.html"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    # Explicit root route for React
    @app.get("/")
    async def serve_react_root():
        response = FileResponse(os.path.join(frontend_dist, "index.html"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

# Legacy Jinja Route (Disabled in favor of React)
# @app.api_route("/", methods=["GET", "HEAD"])
# async def index(request: Request):
#     # Check if we have a saved token
#     from app.core.fyers_handler import fyers_auth
#     token = fyers_auth.load_access_token()
#     
#     # Render LANDING page with strictly limited context (No P&L, No User Details)
#     # The token is only checked to toggle "Connect" vs "Launch" buttons
#     return templates.TemplateResponse("landing.html", {
#         "request": request,
#         "authenticated": token is not None
#     })

if __name__ == "__main__":
    import uvicorn
    # Revert to 8000 as requested
    uvicorn.run(app, host="0.0.0.0", port=8000)
