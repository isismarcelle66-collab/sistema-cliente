from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "site" / "templates")

@router.get("/pipeline")
def pipeline(request: Request):
    return templates.TemplateResponse("pipeline.html", {"request": request})