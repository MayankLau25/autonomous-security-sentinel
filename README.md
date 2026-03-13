# Autonomous Security Sentinel

AI-native security framework for LLM interaction hardening.

## Core Features
- **Hallucination Detection**: Heuristic-based verification of LLM responses against input prompts.
- **Sensitive Data Leakage Detection**: Regex-based scanning for API keys, emails, IP addresses, and AWS secrets.
- **FastAPI-powered API**: Lightweight, high-performance API for real-time validation.
- **Dockerized Deployment**: Ready for containerized environments.
- **CI/CD Integration**: Fully automated testing with GitHub Actions.

## Getting Started

### Prerequisites
- Python 3.10+
- Docker (optional)

### Installation
```bash
pip install -r requirements.txt
```

### Running the API
```bash
PYTHONPATH=src python src/main.py
```

### Running Tests
```bash
pytest tests/
```

### Docker
```bash
docker build -t security-sentinel .
docker run -p 8000:8000 security-sentinel
```

## API Documentation
The API documentation is available at `http://localhost:8000/docs`.

### Validate Output Endpoint
`POST /api/v2/validate-output`

```json
{
    "prompt": "Your input text...",
    "response": "The LLM response..."
}
```
