from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from modules.ingestion import parse_resume
from modules.defense_scanner import sanitize_text
from modules.extractor import extract_entities
from modules.matcher import compute_similarity, rank_candidates

app = FastAPI(title="FairGuard-Rank API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FairGuard-Rank API"}

@app.post("/api/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = parse_resume(content, file.filename)
        
        # 1. Defense Scan
        security_report = sanitize_text(text)
        if not security_report["is_safe"]:
            return {"status": "rejected", "reason": "Security flags detected", "flags": security_report["flags"]}
            
        # 2. Extract Entities
        entities = extract_entities(security_report["clean_text"])
        
        return {
            "status": "success",
            "filename": file.filename,
            "extracted_text": security_report["clean_text"][:500] + "...", # Truncate for response
            "entities": entities
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/rank_candidates")
def rank_endpoint(job_description: str, candidates: List[dict]):
    """
    Expects candidates to be a list of dictionaries with 'id', 'name', and 'text' keys.
    """
    try:
        ranked = rank_candidates(job_description, candidates)
        return {"ranked_candidates": ranked}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
