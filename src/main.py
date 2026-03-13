from fastapi import FastAPI, APIRouter, HTTPException
from src.models.schemas import ScanRequest, ScanResponse, SecurityMetadata
from src.core.security_engine import SecurityEngine

app = FastAPI(
    title="Autonomous Security Sentinel",
    description="AI-native security framework for LLM interaction hardening.",
    version="1.0.0"
)

security_engine = SecurityEngine()

@app.get("/")
async def root():
    return {"message": "Autonomous Security Sentinel is active", "status": "healthy"}

@app.post("/api/v1/scan-prompt", response_model=ScanResponse)
async def scan_prompt(request: ScanRequest):
    """
    Scans a user prompt for injection attacks and PII.
    """
    try:
        response = await security_engine.analyze_prompt(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/validate-code", response_model=SecurityMetadata)
async def validate_code(code: str):
    """
    Scans AI-generated code for security vulnerabilities.
    """
    try:
        return security_engine.validate_code_output(code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
