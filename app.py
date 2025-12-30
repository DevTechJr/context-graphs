from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from services.graph import create_decision, get_decision
from services.orchestration import decide

app = FastAPI(title="Context Graph PoC")

# CORS - Allow Streamlit to call this API from different domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "Context Graph API", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check for Render monitoring"""
    return {"status": "healthy"}


class DecisionIn(BaseModel):
    id: str
    payload: Dict[str, Any]
    database: Optional[str] = None


@app.post("/decisions")
async def post_decision(dec: DecisionIn):
    try:
        create_decision(dec.id, dec.payload, database=dec.database)
        return {"status": "ok", "id": dec.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/decisions/{decision_id}")
async def read_decision(decision_id: str, database: Optional[str] = None):
    try:
        node = get_decision(decision_id, database=database)
        if not node:
            raise HTTPException(status_code=404, detail="Decision not found")
        return node
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class DecideRequest(BaseModel):
    request: str
    evidence: Optional[List[str]] = None
    actor: Optional[str] = "api_user"


@app.post("/decide")
async def make_decision(req: DecideRequest):
    """
    Make an AI-powered decision with full context tracing.
    
    Returns decision ID, result, confidence, reasoning, and metadata about policies/precedents used.
    """
    try:
        result = decide(
            request=req.request,
            evidence=req.evidence,
            actor_id=req.actor
        )
        return {
            "status": "ok",
            "decision_id": result["decision_id"],
            "decision": result["decision"],
            "confidence": result["confidence"],
            "reasoning": result["reasoning"],
            "policies_considered": result["policies_considered"],
            "precedents_found": result["precedents_found"],
            "used_precedents": result["used_precedents"],
            "policies_details": result.get("policies_details", []),
            "precedents_details": result.get("precedents_details", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
