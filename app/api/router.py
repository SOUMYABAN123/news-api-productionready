from fastapi import APIRouter
from app.routes.auth import router as auth_router
from app.routes.news import router as news_router
from app.routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(news_router)
api_router.include_router(health_router)
