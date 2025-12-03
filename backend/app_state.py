"""Application-wide shared state for connectors and agent instances."""
from __future__ import annotations

from backend.agents.self_healing_agent import SelfHealingAgent
from connectors.aws_mock import AWSMockConnector
from connectors.azure_mock import AzureMockConnector
from connectors.gcp_mock import GCPMockConnector

aws_connector = AWSMockConnector()
azure_connector = AzureMockConnector()
gcp_connector = GCPMockConnector()

CONNECTORS = {
    "aws": aws_connector,
    "azure": azure_connector,
    "gcp": gcp_connector,
}

AGENT = SelfHealingAgent(CONNECTORS)
