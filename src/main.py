from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.core.advanced_detectors import AdvancedDetectors

app = FastAPI(
    title="Autonomous Security Sentinel",
    description="AI-native security framework for LLM interaction hardening.",
    version="2.0.0"
)

# Initialize detectors
advanced_detectors = AdvancedDetectors()

class ValidationRequest(BaseModel):
    prompt: str
    response: str

@app.get("/")
async def root():
    return {
        "message": "Autonomous Security Sentinel v2.0 is active",
        "status": "healthy",
        "features": ["hallucination_detection", "leakage_prevention", "pii_scrubbing"]
    }

@app.post("/api/v2/validate-output")
async def validate_output(request: ValidationRequest):
    """
    Validates LLM output for hallucinations and sensitive data leakage.
    """
    try:
        results = advanced_detectors.analyze_output(request.prompt, request.response)
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
