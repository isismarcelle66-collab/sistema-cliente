from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_PATH = os.path.join(BASE_DIR, "..", "site", "templates")

templates = Jinja2Templates(directory=TEMPLATES_PATH)

@router.get("/pipeline")
def pipeline(request: Request):
    return templates.TemplateResponse("pipeline.html", {"request": request})
