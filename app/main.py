from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.database import init_db

# routers
from app.routes import leads
from app.routes import dashboard
from app.routes import metricas


app = FastAPI()

# inicia banco
init_db()

# caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_PATH = os.path.join(BASE_DIR, "..", "site", "templates")
STATIC_PATH = os.path.join(BASE_DIR, "..", "site", "static")

templates = Jinja2Templates(directory=TEMPLATES_PATH)

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

# inclui rotas
app.include_router(leads.router)
app.include_router(dashboard.router)
app.include_router(metricas.router)


@app.get("/")
def root():
    return {"status": "ERP rodando 🚀"}
