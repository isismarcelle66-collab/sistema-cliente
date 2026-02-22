from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from app.database import get_connection
from pathlib import Path

router = APIRouter()

# Caminho templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "site" / "templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ===============================
# REGISTRO
# ===============================
@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register_user(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = pwd_context.hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()
    except:
        conn.close()
        raise HTTPException(status_code=400, detail="Usuário já existe")

    conn.close()
    return RedirectResponse(url="/login", status_code=303)


# ===============================
# LOGIN
# ===============================
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    response = RedirectResponse(url="/pipeline", status_code=303)
    response.set_cookie(key="user", value=username)

    return response


# ===============================
# LOGOUT
# ===============================
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("user")
    return response