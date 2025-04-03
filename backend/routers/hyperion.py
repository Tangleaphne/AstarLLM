# backend/routers/hyperion.py
from fastapi import APIRouter, Body
from backend.services import hyperion_text

router = APIRouter()

@router.post("/analyze/frontend")
async def analyze_frontend_description(text: str = Body(...)):
    result = hyperion_text.extract_description_facts(text)
    return {"frontend_claims": result}