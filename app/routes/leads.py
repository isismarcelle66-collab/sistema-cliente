from fastapi import APIRouter, Request, HTTPException
from app.database import get_connection

router = APIRouter()


# ===============================
# LISTAR LEADS DO USUÁRIO
# ===============================
@router.get("/api/leads")
def listar_leads(request: Request):
    username = request.cookies.get("user")

    if not username:
        raise HTTPException(status_code=401, detail="Não autenticado")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    cursor.execute(
        "SELECT id, nome, email, telefone, status FROM leads WHERE user_id = %s",
        (user[0],)
    )

    leads = cursor.fetchall()

    cursor.close()
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


# ===============================
# CRIAR LEAD
# ===============================
@router.post("/api/leads")
def criar_lead(request: Request, nome: str, email: str, telefone: str):
    username = request.cookies.get("user")

    if not username:
        raise HTTPException(status_code=401, detail="Não autenticado")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    cursor.execute(
        "INSERT INTO leads (nome, email, telefone, status, user_id) VALUES (%s, %s, %s, %s, %s)",
        (nome, email, telefone, "novo", user[0]),
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Lead criado com sucesso"}


# ===============================
# ATUALIZAR STATUS
# ===============================
@router.put("/api/leads/{lead_id}")
def atualizar_status(lead_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE leads SET status = %s WHERE id = %s",
        (status, lead_id),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Status atualizado com sucesso"}