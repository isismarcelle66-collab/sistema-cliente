from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter()


# ===============================
# LISTAR LEADS
# ===============================
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


# ===============================
# CRIAR LEAD
# ===============================
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