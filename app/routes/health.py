from fastapi import APIRouter
from app.services.ml_service import model_info

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    info = model_info()
    return {"status": "ok", **info}
