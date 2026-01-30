from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.api.router import router

app = FastAPI(title="Clicker Game")
# API routes
app.include_router(router)
# Templates
templates = Jinja2Templates(directory="backend/templates")
# Static files
app.mount("/static", StaticFiles(directory="backend/templates/static"), name="static")
