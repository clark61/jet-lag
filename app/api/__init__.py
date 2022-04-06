from fastapi import APIRouter

from app.api import airlines

api_router = APIRouter()
api_router.include_router(airlines.router, prefix="/airlines", tags=[airlines])