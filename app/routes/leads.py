@router.post("/api/leads")
def criar_lead(nome: str, email: str, telefone: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO leads (nome, email, telefone, status) VALUES (?, ?, ?, ?)",
        (nome, email, telefone, "novo")
    )

    conn.commit()
    conn.close()

    return {"message": "Lead criado com sucesso"}