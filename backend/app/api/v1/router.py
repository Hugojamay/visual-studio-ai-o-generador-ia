from fastapi import APIRouter
from app.api.v1.endpoints import art_director

api_router = APIRouter()
api_router.include_router(art_director.router, prefix="/art-director", tags=["Director de Arte"])