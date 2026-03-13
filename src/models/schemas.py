from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ScanRequest(BaseModel):
    text: str = Field(..., description="The input text to be scanned for security risks.")
    context: Optional[str] = Field(None, description="Optional context for the LLM interaction.")

class SecurityMetadata(BaseModel):
    is_safe: bool
    risk_score: float = Field(0.0, ge=0.0, le=1.0)
    detected_threats: List[str] = []
    sanitized_text: Optional[str] = None

class ScanResponse(BaseModel):
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "completed"
    results: SecurityMetadata

class AuditLogEntry(BaseModel):
    timestamp: datetime
    request_id: str
    input_hash: str
    security_score: float
    threats: List[str]
    action_taken: str
