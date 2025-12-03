# API Reference

All endpoints are served by FastAPI. Payloads use JSON; examples are self-contained to keep the system fully simulated.

## Health
- **GET** `/health`
- **Response:** `{ "status": "ok" }`

## Alert Intake
- **POST** `/alert`
- **Body:**
  ```json
  {
    "id": "alert-123",
    "issue_type": "Publicly exposed storage",
    "resource": {"provider": "aws", "id": "s3-001", "name": "open-bucket"},
    "source": "demo-monitor"
  }
  ```
- **Response:** Echo with `{ "received": true, "alert": { ... } }`

## Run Autonomous Agent
- **POST** `/run_agent`
- **Body:** Same shape as `/alert`.
- **Response:** `AgentRunResult`
  - `validated`: whether alert validation passed
  - `issues`: detected issues with severity and recommended fix
  - `generated_fix`: IaC plan metadata (tool, content, output_path)
  - `remediation_applied`: whether fixes were applied (simulated)
  - `decisions`: ordered decision log for auditability
  - `compliance_notes`: mapping to frameworks
  - `ticket_update`: synthetic ticket summary
- **Errors:** `400 Bad Request` when mandatory alert attributes are missing.

## Detection
- **GET** `/issues`
- **Response:** List of `Issue` objects for all mock connectors.

## Fix Generation
- **POST** `/fix`
- **Body:** Array of `Issue` objects.
- **Response:** Generated `FixPlan` with Terraform content and output path.
- **GET** `/fix/latest` – Returns the latest persisted `FixPlan` or `null`.

## Compliance
- **GET** `/compliance`
- **Response:**
  ```json
  {
    "mapping": {"ACSC Essential Eight": ["Multi-factor authentication"], ...},
    "risk_score": 25,
    "issue_count": 5
  }
  ```

## Dashboard
- **GET** `/dashboard`
- **Response:** Aggregated issues, compliance mapping, risk score, and latest fix content (if present) for easy rendering in the static UI.

## Safety Notes
- No real cloud calls are made; connectors are deterministic mocks.
- Terraform plans are saved locally under `iac_versions/` for replay and review.
