# routers/dashboard.py

from fastapi import APIRouter
from datetime import datetime
from collections import Counter

router = APIRouter()

# exemplo de dados, substitua pela sua base real
fake_users = [
    {"id": 1, "created_at": "2025-12-01"},
    {"id": 2, "created_at": "2025-12-03"},
    {"id": 3, "created_at": "2025-11-15"},
]

@router.get("/stats/customers-per-month")
def customers_per_month():
    months = [datetime.strptime(u["created_at"], "%Y-%m-%d").strftime("%Y-%m") for u in fake_users]
    counts = dict(Counter(months))
    return counts
