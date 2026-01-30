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

@router.get("/ranking", response_class=HTMLResponse)
def ranking_page(request: Request):
    return templates.TemplateResponse(
        "ranking.html",
        {"request": request},
    )

@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request},
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request},
    )

