"""Server-side access point for the WebTutor environment.

This module keeps the server layer thin. It simply re-exports the shared
environment and data models from the project root so the same logic is used
locally and when running under FastAPI or a future OpenEnv wrapper.
"""

from __future__ import annotations

from environment import WebTutorEnv
from models import Action, Observation, State

__all__ = ["WebTutorEnv", "Action", "Observation", "State"]