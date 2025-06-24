# Growth Force Reporting Agent - Backend

FastAPI backend for the Growth Force Reporting Agent.

## Setup

1. Install dependencies with uv:
```bash
uv sync
```

2. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run the development server:
```bash
uv run uvicorn src.main:app --reload
```

## API Endpoints

- `POST /api/reports/generate` - Generate report from natural language query
- `GET /api/reports/session/{session_id}` - Get session information
- `GET /health` - Health check

## Development

Run linting and formatting:
```bash
uv run ruff check .
uv run black .
uv run mypy .
```

Run tests:
```bash
uv run pytest
```