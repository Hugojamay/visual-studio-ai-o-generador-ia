from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.prompt_engine import ArtDirectorEngine

router = APIRouter()
engine = ArtDirectorEngine()

class ArtDirectorRequest(BaseModel):
    user_instruction: str
    category: str = "Fotografía de productos"
    aspect_ratio: str = "1:1"
    realism_level: int = 9
    image_url: Optional[str] = None  # Nuevo: Permite recibir una imagen base

class ArtDirectorResponse(BaseModel):
    positive_prompt: str
    negative_prompt: str
    camera_spec: str
    lighting_spec: str
    width: int
    height: int
    image_url: str

@router.post("/optimize", response_model=ArtDirectorResponse)
async def optimize_prompt(payload: ArtDirectorRequest):
    result = engine.optimize(
        user_instruction=payload.user_instruction,
        category=payload.category,
        aspect_ratio=payload.aspect_ratio,
        realism_level=payload.realism_level,
        image_url=payload.image_url  # Se lo pasamos al motor
    )
    return result