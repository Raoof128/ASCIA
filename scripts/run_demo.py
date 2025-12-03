"""Run the self-healing agent locally with a sample alert payload."""
from __future__ import annotations

import json
from pathlib import Path

from backend.app_state import AGENT
from backend.models import Alert


def load_sample_alert() -> Alert:
    """Load the bundled sample alert payload and validate its structure."""
    sample_path = Path("examples/alert_public_storage.json")
    payload = json.loads(sample_path.read_text(encoding="utf-8"))
    return Alert(**payload)


def main() -> None:
    """Execute the agent against the bundled sample alert and print the result."""
    alert = load_sample_alert()
    result = AGENT.run(alert)
    print("Decisions:")
    for decision in result.decisions:
        print(f" - {decision.step}: {decision.detail} (success={decision.success})")
    print("\nGenerated fix:\n")
    if result.generated_fix:
        print(result.generated_fix.content)
    else:
        print("No fix generated")


if __name__ == "__main__":
    main()
