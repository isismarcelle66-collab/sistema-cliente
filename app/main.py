from fastapi import FastAPI, Form, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
import sqlite3
import csv
from io import StringIO
from datetime import datetime

# =====================
# PATHS
# =====================
BASE_DIR = Path(__file__).resolve().parent
SITE_DIR = BASE_DIR / "site"
DB_PATH = BASE_DIR / "clientes.db"

# =====================
# APP
# =====================
app = FastAPI(title="Sistema de Clientes")

app.add_middleware(
    SessionMiddleware,
    secret_key="chave-demo"
)

app.mount("/site", StaticFiles(directory=SITE_DIR), name="site")

# =====================
# DB
# =====================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn, conn.cursor()

@app.on_event("startup")
def startup():
    conn, cursor = get_db()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            telefone TEXT,
            created_at TEXT DEFAULT (date('now'))
        )
    """)
    conn.commit()
    conn.close()

# =====================
# ROTAS
# =====================
@app.get("/")
def home():
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
def login():
    return (SITE_DIR / "login.html").read_text(encoding="utf-8")

@app.post("/login")
def login_post(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...)
):
    request.session["user"] = email
    return RedirectResponse("/dashboard", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")
    return (SITE_DIR / "dashboard.html").read_text(encoding="utf-8")

@app.post("/lead")
def lead(
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...)
):
    conn, cursor = get_db()
    cursor.execute(
        "INSERT INTO clientes (nome, email, telefone, created_at) VALUES (?, ?, ?, ?)",
        (nome, email, telefone, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()
    return {"ok": True}

# =====================
# API Métricas
# =====================
@app.get("/api/metricas")
def metricas():
    conn, cursor = get_db()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    conn.close()
    return {"clientes": total}

@app.get("/api/metricas/mes")
def clientes_por_mes():
    conn, cursor = get_db()
    cursor.execute("SELECT created_at FROM clientes")
    datas = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    contagem = {}
    for data in datas:
        mes = datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m")
        contagem[mes] = contagem.get(mes, 0) + 1
    
    return contagem

# =====================
# Exportação CSV
# =====================
@app.get("/api/export")
def export_csv():
    conn, cursor = get_db()
    cursor.execute("SELECT id, nome, email, telefone, created_at FROM clientes")
    linhas = cursor.fetchall()
    conn.close()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["ID", "Nome", "Email", "Telefone", "Data"])
    writer.writerows(linhas)
    si.seek(0)

    return StreamingResponse(
        si,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=clientes.csv"}
    )

# =====================
# Endpoint JSON para dashboard
# =====================
@app.get("/api/clientes-json")
def clientes_json(
    busca: str = Query("", alias="busca"),
    inicio: str = Query("", alias="inicio"),
    fim: str = Query("", alias="fim")
):
    conn, cursor = get_db()
    query = "SELECT nome, email, telefone, created_at FROM clientes WHERE 1=1"
    params = []

    if busca:
        query += " AND (nome LIKE ? OR email LIKE ? OR telefone LIKE ?)"
        termo = f"%{busca}%"
        params.extend([termo, termo, termo])

    if inicio:
        query += " AND created_at >= ?"
        params.append(inicio)
    if fim:
        query += " AND created_at <= ?"
        params.append(fim)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    clientes_list = [
        {"Nome": r[0], "Email": r[1], "Telefone": r[2], "Data": r[3]}
        for r in rows
    ]
    return {"clientes": clientes_list}
