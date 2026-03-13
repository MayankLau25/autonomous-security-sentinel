import re
from typing import List, Tuple

class PromptInjectionDetector:
    """Detects common prompt injection and jailbreak patterns."""
    
    INJECTION_PATTERNS = [
        r"(?i)ignore\s+previous\s+instructions",
        r"(?i)you\s+are\s+now\s+a\s+unfiltered",
        r"(?i)system\s+override",
        r"(?i)bypass\s+safety",
        r"(?i)dan\s+mode",
        r"(?i)respond\s+as\s+.*without\s+restrictions",
    ]

    def scan(self, text: str) -> Tuple[bool, List[str], float]:
        detected = []
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text):
                detected.append(f"Prompt Injection Pattern: {pattern}")
        
        risk_score = min(1.0, len(detected) * 0.4)
        is_safe = len(detected) == 0
        return is_safe, detected, risk_score

class PIIScanner:
    """Scans for Personally Identifiable Information (PII)."""
    
    PATTERNS = {
        "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "Credit Card": r"\b(?:\d[ -]*?){13,16}\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "Phone Number": r"\b(?:\+?\d{1,3}[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b"
    }

    def scan(self, text: str) -> Tuple[bool, List[str], str]:
        detected = []
        sanitized_text = text
        for pii_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                detected.append(f"Detected PII: {pii_type}")
                # Simple redaction
                sanitized_text = re.sub(pattern, f"[{pii_type}_REDACTED]", sanitized_text)
        
        is_safe = len(detected) == 0
        return is_safe, detected, sanitized_text

class MaliciousCodeScanner:
    """Scans AI-generated code for common security anti-patterns."""
    
    VULNERABILITIES = [
        (r"(?i)exec\s*\(", "Dangerous function usage (exec)"),
        (r"(?i)eval\s*\(", "Dangerous function usage (eval)"),
        (r"(?i)os\.system\s*\(", "System call vulnerability"),
        (r"(?i)subprocess\.Popen\s*\(.*shell=True", "Shell injection risk"),
        (r"(?i)api_key\s*=\s*['\"][a-zA-Z0-9]{16,}['\"]", "Hardcoded API Key")
    ]

    def scan(self, code: str) -> List[str]:
        findings = []
        for pattern, label in self.VULNERABILITIES:
            if re.search(pattern, code):
                findings.append(label)
        return findings
