"""Simple client wrapper for the WebTutor environment."""

from __future__ import annotations
from typing import Any, Dict, Optional, Tuple

try:
    from server.environment import WebTutorEnv
except Exception:
    from environment import WebTutorEnv


class WebTutorClient:
    """Tiny helper that wraps a local WebTutorEnv instance."""

    def __init__(self, seed: Optional[int] = None):
        self.env = WebTutorEnv(seed=seed)

    def reset(self, task_index: Optional[int] = None) -> Dict[str, Any]:
        return self.env.reset(task_index=task_index)

    def step(self, action: Any) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        return self.env.step(action)

    def state(self) -> Dict[str, Any]:
        return self.env.state()


if __name__ == "__main__":
    client = WebTutorClient(seed=42)
    obs = client.reset(task_index=0)
    print("Initial observation:", obs)