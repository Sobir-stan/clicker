from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="backend/templates")

router = APIRouter(tags=["pages"])


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request},
    )


@router.get("/clicker", response_class=HTMLResponse)
def clicker_page(request: Request):
    return templates.TemplateResponse(
        "clicker.html",
        {"request": request},
    )
