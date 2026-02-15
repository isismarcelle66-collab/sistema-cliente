from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import os

from app.database import init_db

# Routers
from app.routes import leads
from app.routes import dashboard
from app.routes import metricas


app = FastAPI(title="Sistema ERP - Gestão de Leads")

# ==============================
# INICIALIZA BANCO NO STARTUP
# ==============================
@app.on_event("startup")
def startup():
    init_db()


# ==============================
# CONFIGURAÇÃO DE CAMINHOS
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SITE_DIR = os.path.join(BASE_DIR, "..", "site")
TEMPLATES_PATH = os.path.join(SITE_DIR, "templates")
STATIC_PATH = os.path.join(SITE_DIR, "static")

# Verifica se as pastas existem antes de montar
if os.path.exists(TEMPLATES_PATH):
    templates = Jinja2Templates(directory=TEMPLATES_PATH)
else:
    templates = None
    print("⚠ Pasta templates não encontrada.")

if os.path.exists(STATIC_PATH):
    app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
else:
    print("⚠ Pasta static não encontrada.")


# ==============================
# INCLUI ROUTERS
# ==============================
app.include_router(leads.router)
app.include_router(dashboard.router)
app.include_router(metricas.router)


# ==============================
# ROTA RAIZ
# ==============================
@app.get("/")
def root():
    return RedirectResponse(url="/docs")
