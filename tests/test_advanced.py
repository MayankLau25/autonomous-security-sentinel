import pytest
from src.core.advanced_detectors import AdvancedDetectors

@pytest.fixture
def detector():
    return AdvancedDetectors()

def test_leakage_detection(detector):
    text_with_key = "My API key is api-key: abcdef1234567890abcdef1234567890"
    leaks = detector.detect_leakage(text_with_key)
    assert "api_key" in leaks
    assert leaks["api_key"][0] == "abcdef1234567890abcdef1234567890"

def test_hallucination_detection(detector):
    prompt = "The population of Paris is 2.1 million."
    # High hallucination: 42 is not in prompt
    response = "Paris has 42 million people."
    score = detector.detect_hallucination(prompt, response)
    assert score > 0

    # Low hallucination: 2.1 is in prompt
    response_safe = "Paris has 2.1 million people."
    score_safe = detector.detect_hallucination(prompt, response_safe)
    assert score_safe == 0.0

def test_analyze_output(detector):
    prompt = "Tell me about my server."
    response = "Your server IP is 192.168.1.1 and it has 5 cores."
    analysis = detector.analyze_output(prompt, response)
    
    assert "leakage" in analysis
    assert "ip_address" in analysis["leakage"]
    assert analysis["hallucination_score"] > 0
    assert analysis["safe"] is False
