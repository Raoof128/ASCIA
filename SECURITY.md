# Security Policy

## Supported Versions
ASCIA is a simulated platform and does not connect to live cloud environments. Security updates and fixes are applied to the `main` branch, and contributors should open pull requests against this branch.

## Reporting a Vulnerability
If you discover a security issue:
1. Email **security@ascia.example.com** with a detailed description, reproduction steps, and potential impact.
2. We will acknowledge receipt within 72 hours and provide a remediation ETA after triage.
3. Please avoid public disclosure until a fix is released or a coordinated date is agreed.

## Secure Development Practices
- No secrets, credentials, or live endpoints are stored in the repository.
- All cloud interactions are mock implementations; never substitute real credentials in tests.
- Input validation and logging safeguards are expected for every new endpoint and engine.
- Dependencies should be kept current; run `pip list --outdated` periodically and bump versions via pull request.
- When modifying IaC generation, default to secure, least-privilege configurations and document assumptions.

## Incident Response (Simulated)
- Reproduce the issue using the provided tests or additional fixtures.
- Add regression tests to prevent recurrence and include clear remediation notes in the PR description.
- Update documentation if the vulnerability affects user-facing flows or operational guidance.
