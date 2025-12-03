# Operations & Usage Guide

This guide provides quick-start commands, example payloads, and operational practices for running ASCIA locally.

## Quick Start
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies (including dev tools):
   ```bash
   pip install -e .[dev]
   ```
3. Launch the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
4. Open the dashboard by serving `frontend/` (for example `python -m http.server 8001`) and setting the API base URL.

## Example Alert Payload
Send an alert to kick off the agent loop:
```bash
curl -X POST http://localhost:8000/run_agent \
  -H 'Content-Type: application/json' \
  -d '{
        "id": "demo-001",
        "issue_type": "Publicly exposed storage",
        "resource": {"id": "s3-001", "name": "open-bucket", "type": "s3"},
        "source": "demo"
      }'
```

## Common Workflows
- **View detected issues**: `curl http://localhost:8000/issues`
- **Fetch latest IaC fix**: `curl http://localhost:8000/fix/latest`
- **Review compliance mapping**: `curl http://localhost:8000/compliance`
- **Health check**: `curl http://localhost:8000/health`

## Operational Best Practices
- Keep `logs/app.log` rotated via the built-in rotating file handler; adjust the log path through `backend.utils.logging_utils.setup_logging`.
- All generated IaC artifacts land in `iac_versions/` with timestamped filenames for replay and audit. Do not store secrets alongside IaC artifacts.
- When adding new detection rules or connectors, ensure the mock implementations remain deterministic for tests and demos.
- Use the included `docs/API.md` for full request/response schemas when integrating clients.

## Troubleshooting
- If the API fails to start, verify the virtual environment is active and dependencies are installed.
- For failing tests, re-run `ruff check .` to catch lint or security rule violations before debugging further.
- Missing IaC outputs usually indicate validation failures; review the agent decisions returned by `/run_agent` for context.
