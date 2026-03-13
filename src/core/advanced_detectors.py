import re
import hashlib
from typing import List, Dict

class AdvancedDetectors:
    def __init__(self):
        # Patterns for potential sensitive data leakage
        self.leakage_patterns = {
            "api_key": re.compile(r"(?:api[_-]?key|access[_-]?token|secret[_-]?key)[\s:=]+['\"]?([a-zA-Z0-9_\-]{32,})['\"]?", re.I),
            "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
            "ip_address": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
            "aws_secret": re.compile(r"AKIA[0-9A-Z]{16}"),
        }

    def detect_leakage(self, text: str) -> Dict[str, List[str]]:
        """Detect potential sensitive data leakage in text."""
        leaks = {}
        for key, pattern in self.leakage_patterns.items():
            matches = pattern.findall(text)
            if matches:
                leaks[key] = matches
        return leaks

    def detect_hallucination(self, prompt: str, response: str) -> float:
        """
        Simple heuristic for hallucination detection.
        Returns a score between 0 and 1, where 1 means highly likely hallucinated.
        In a real scenario, this would involve NLI (Natural Language Inference) 
        or fact-checking against a knowledge base.
        """
        # Heuristic: Check for consistency in named entities or numerical values
        # This is a placeholder for more advanced logic
        prompt_numbers = set(re.findall(r"\b\d+\b", prompt))
        response_numbers = set(re.findall(r"\b\d+\b", response))
        
        # If response contains numbers not in prompt, it *might* be a hallucination
        # depending on the context.
        unverifiable_numbers = response_numbers - prompt_numbers
        
        if not response_numbers:
            return 0.0
            
        score = len(unverifiable_numbers) / len(response_numbers)
        return min(score, 1.0)

    def analyze_output(self, prompt: str, response: str) -> Dict:
        """Run all advanced detections on LLM output."""
        return {
            "leakage": self.detect_leakage(response),
            "hallucination_score": self.detect_hallucination(prompt, response),
            "safe": len(self.detect_leakage(response)) == 0 and self.detect_hallucination(prompt, response) < 0.5
        }
