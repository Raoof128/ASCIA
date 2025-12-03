"""FastAPI entrypoint for the ASCIA platform."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import agent, compliance, dashboard, detect, fix
from backend.utils.logging_utils import setup_logging

setup_logging()

app = FastAPI(title="Autonomous Self-Healing Cloud Infrastructure Agent", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent.router)
app.include_router(detect.router)
app.include_router(fix.router)
app.include_router(compliance.router)
app.include_router(dashboard.router)


@app.get("/health", response_model=dict)
async def health() -> dict:
    """Health endpoint for uptime monitoring."""
    return {"status": "ok"}
