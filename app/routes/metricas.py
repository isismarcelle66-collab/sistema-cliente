from fastapi import APIRouter
import sqlite3
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "clientes.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

@router.get("/metricas")
def api_metricas():
    conn, cursor = get_db()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    conn.close()

    return {
        "clientes_unicos": total,
        "clientes_recompra": max(total - 1, 0),
        "total_pedidos": total
    }
