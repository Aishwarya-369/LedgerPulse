import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.routers.api import router as api_router

app = FastAPI(title="LedgerPulse AI")

# Mount API router
app.include_router(api_router, prefix="/api")

# Directory paths
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Direct root routes for PWA
@app.get("/manifest.json")
def serve_manifest():
    return FileResponse(os.path.join(frontend_dir, "manifest.json"), media_type="application/manifest+json")

@app.get("/sw.js")
def serve_sw():
    return FileResponse(os.path.join(frontend_dir, "sw.js"), media_type="application/javascript")

# Web Pages
@app.get("/")
def serve_landing():
    return FileResponse(os.path.join(frontend_dir, "landing.html"))

@app.get("/login")
def serve_login():
    return FileResponse(os.path.join(frontend_dir, "login.html"))

@app.get("/app")
def serve_app():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
