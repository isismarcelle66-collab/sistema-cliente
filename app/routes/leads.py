from fastapi import APIRouter
from app.database import get_connection

router = APIRouter()


@router.get("/api/leads")
def listar_leads():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nome, email, telefone, status FROM leads"
    )
    leads = cursor.fetchall()
    conn.close()

    return [
        {
            "id": l[0],
            "nome": l[1],
            "email": l[2],
            "telefone": l[3],
            "status": l[4],
        }
        for l in leads
    ]


@router.post("/api/leads")
def criar_lead(nome: str, email: str, telefone: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO leads (nome, email, telefone, status) VALUES (?, ?, ?, ?)",
        (nome, email, telefone, "novo"),
    )

    conn.commit()
    conn.close()

    return {"message": "Lead criado com sucesso"}