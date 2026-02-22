from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter()


# ===============================
# LISTAR LEADS
# ===============================
@router.post("/api/leads")
def criar_lead(request: Request, nome: str, email: str, telefone: str):
    username = request.cookies.get("user")

    if not username:
        raise HTTPException(status_code=401, detail="Não autenticado")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    cursor.execute(
        "INSERT INTO leads (nome, email, telefone, status, user_id) VALUES (?, ?, ?, ?, ?)",
        (nome, email, telefone, "novo", user["id"]),
    )

    conn.commit()
    conn.close()

    return {"message": "Lead criado com sucesso"}
# ===============================
# CRIAR LEAD
# ===============================
@router.get("/api/leads")
def listar_leads(request: Request):
    username = request.cookies.get("user")

    if not username:
        raise HTTPException(status_code=401, detail="Não autenticado")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    cursor.execute(
        "SELECT id, nome, email, telefone, status FROM leads WHERE user_id = ?",
        (user["id"],),
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
# ===============================
# ATUALIZAR STATUS (Drag & Drop)
# ===============================
@router.put("/api/leads/{lead_id}")
def atualizar_status(lead_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE leads SET status = ? WHERE id = ?",
        (status, lead_id),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    conn.commit()
    conn.close()

    return {"message": "Status atualizado com sucesso"}


# ===============================
# DELETAR LEAD (extra profissional)
# ===============================
@router.delete("/api/leads/{lead_id}")
def deletar_lead(lead_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    conn.commit()
    conn.close()

    return {"message": "Lead removido com sucesso"}