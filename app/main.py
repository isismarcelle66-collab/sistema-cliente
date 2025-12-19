# -*- coding: utf-8 -*-

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List
import sqlite3
import uuid
import os
import requests  # para Bling

# =========================
# APP
# =========================
app = FastAPI(
    title="Sistema de Clientes",
    description="API para construção de base própria de clientes e integração Bling",
    version="1.0.0"
)
SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "site")

app.mount(
    "/site",
    StaticFiles(directory=SITE_DIR, html=True),
    name="site"
)

# =========================
# CAMINHO BASE DO PROJETO (AJUSTE 4)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# BANCO DE DADOS
# =========================
conn = sqlite3.connect("clientes.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    cpf TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL
)
""")
conn.commit()

# =========================
# SCHEMAS
# =========================
class ClienteCreate(BaseModel):
    cpf: str = Field(..., example="12345678901", min_length=11, max_length=11)
    nome: str = Field(..., example="João da Silva", min_length=3)
    email: EmailStr = Field(..., example="joao@email.com")
    telefone: str = Field(..., example="11999999999", min_length=10, max_length=11)

    @validator("cpf")
    def validar_cpf(cls, v):
        if not v.isdigit():
            raise ValueError("CPF deve conter apenas números")
        if len(v) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        return v


class ClienteResponse(ClienteCreate):
    pass

# =========================
# FUNÇÕES AUXILIARES
# =========================
def salvar_cliente(cliente: ClienteCreate):
    try:
        cursor.execute(
            """
            INSERT INTO clientes (cpf, nome, email, telefone)
            VALUES (?, ?, ?, ?)
            """,
            (cliente.cpf, cliente.nome, cliente.email, cliente.telefone)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Cliente com este CPF já existe"
        )


def listar_clientes():
    cursor.execute("SELECT cpf, nome, email, telefone FROM clientes")
    return cursor.fetchall()

# =========================
# CONFIGURAÇÃO BLING
# =========================
API_KEY = "SEU_TOKEN_AQUI"
BLING_BASE_URL = "https://bling.com.br/Api/v2"

def buscar_leads_bling():
    url = f"{BLING_BASE_URL}/clientes/json/"
    params = {"apikey": API_KEY}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        dados = resp.json()
        clientes = dados.get("retorno", {}).get("clientes", [])
        return clientes
    return []

# =========================
# ENDPOINTS API
# =========================
@app.get("/", summary="Health check")
def health():
    return {"status": "Sistema rodando com sucesso"}

@app.post("/clientes", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate):
    salvar_cliente(cliente)
    return cliente

@app.get("/clientes", response_model=List[ClienteResponse])
def buscar_clientes():
    clientes = listar_clientes()
    return [
        ClienteResponse(
            cpf=cpf,
            nome=nome,
            email=email,
            telefone=telefone
        )
        for cpf, nome, email, telefone in clientes
    ]

# =========================
# MÉTRICAS
# =========================
@app.get("/metricas")
def metricas():
    cursor.execute("SELECT COUNT(*) FROM clientes")
    clientes_unicos = cursor.fetchone()[0]

    total_pedidos = 3
    clientes_recompra = max(clientes_unicos - 1, 0)

    taxa_recompra = (
        round((clientes_recompra / clientes_unicos) * 100, 2)
        if clientes_unicos > 0 else 0
    )

    return {
        "clientes_unicos": clientes_unicos,
        "total_pedidos": total_pedidos,
        "clientes_recompra": clientes_recompra,
        "taxa_recompra": f"{taxa_recompra}%"
    }

# =========================
# DASHBOARD
# =========================
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    leads = buscar_leads_bling()
    total_leads = len(leads)

    return f"""
    <html>
        <head>
            <title>Dashboard - Clientes Bling</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body style="font-family: Arial; padding: 40px;">
            <h1>📊 Clientes do Bling</h1>
            <p>Total de leads: {total_leads}</p>
            <canvas id="grafico"></canvas>

            <script>
                new Chart(document.getElementById("grafico"), {{
                    type: "bar",
                    data: {{
                        labels: ["Total Leads"],
                        datasets: [{{
                            label: "Quantidade",
                            data: [{total_leads}]
                        }}]
                    }}
                }});
            </script>
        </body>
    </html>
    """

# =========================
# LEAD
# =========================
@app.post("/lead")
def receber_lead(
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...)
):
    cpf_fake = str(uuid.uuid4().int)[:11]

    cursor.execute(
        "INSERT INTO clientes (cpf, nome, email, telefone) VALUES (?, ?, ?, ?)",
        (cpf_fake, nome, email, telefone)
    )
    conn.commit()

    return RedirectResponse(url="/site", status_code=302)
