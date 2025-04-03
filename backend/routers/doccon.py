# backend/routers/doccon.py
from fastapi import APIRouter, File, UploadFile
from backend.services import fact_extractor, doc_parser

router = APIRouter()

@router.post("/analyze/solidity")
async def analyze_contract(file: UploadFile = File(...)):
    source_code = await file.read()
    result = fact_extractor.extract_facts_from_solidity(source_code.decode())
    return {"code_facts": result}

@router.post("/analyze/documentation")
async def analyze_doc(file: UploadFile = File(...)):
    content = await file.read()
    result = doc_parser.extract_facts_from_doc(content.decode())
    return {"doc_facts": result}
