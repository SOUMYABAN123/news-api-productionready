from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

# demo users (production: DB + hashed passwords)
_DEMO_USER = {"username": "admin", "password": "admin"}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    if payload.username != _DEMO_USER["username"] or payload.password != _DEMO_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=payload.username)
    return TokenResponse(access_token=token)
