import uuid
from typing import Optional
from src.core.detectors import PromptInjectionDetector, PIIScanner, MaliciousCodeScanner
from src.models.schemas import SecurityMetadata, ScanRequest, ScanResponse

class SecurityEngine:
    def __init__(self):
        self.injection_detector = PromptInjectionDetector()
        self.pii_scanner = PIIScanner()
        self.code_scanner = MaliciousCodeScanner()

    async def analyze_prompt(self, request: ScanRequest) -> ScanResponse:
        request_id = str(uuid.uuid4())
        text = request.text
        
        # 1. Check for prompt injection
        inj_is_safe, inj_threats, inj_score = self.injection_detector.scan(text)
        
        # 2. Check for PII
        pii_is_safe, pii_threats, sanitized_text = self.pii_scanner.scan(text)
        
        # Aggregate results
        detected_threats = inj_threats + pii_threats
        is_safe = inj_is_safe and pii_is_safe
        max_risk_score = max(inj_score, 0.5 if not pii_is_safe else 0.0)

        metadata = SecurityMetadata(
            is_safe=is_safe,
            risk_score=max_risk_score,
            detected_threats=detected_threats,
            sanitized_text=sanitized_text if not is_safe else text
        )

        return ScanResponse(
            request_id=request_id,
            results=metadata
        )

    def validate_code_output(self, code: str) -> SecurityMetadata:
        findings = self.code_scanner.scan(code)
        is_safe = len(findings) == 0
        risk_score = 1.0 if not is_safe else 0.0
        
        return SecurityMetadata(
            is_safe=is_safe,
            risk_score=risk_score,
            detected_threats=findings
        )
