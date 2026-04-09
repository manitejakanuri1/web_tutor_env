"""Data models for the web_tutor_env environment.

Upgraded: multi-phase State, expanded Action (8 types), phase-aware Observation.
"""

from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Action:
    """A single environment action.

    Supported action types:
    - navigate       : Move between phases. Requires target ("quiz" or "study").
    - read_section   : Read a study section. Requires section_id.
    - select_answer  : Select option for a question. Requires question_id + option_index.
    - toggle_answer  : Toggle option for multi-select. Requires question_id + option_index.
    - submit_quiz    : Submit all quiz answers for grading.
    - use_hint       : Get a hint for a question. Requires question_id. Costs 2 energy.
    - retry_quiz     : After review, retry with penalty.
    - restart_task   : Fully restart the current task.
    """

    action_type: str
    section_id: Optional[str] = None
    question_id: Optional[str] = None
    option_index: Optional[int] = None
    target: Optional[str] = None

    @classmethod
    def navigate(cls, target: str) -> "Action":
        return cls(action_type="navigate", target=target)

    @classmethod
    def read_section(cls, section_id: str) -> "Action":
        return cls(action_type="read_section", section_id=section_id)

    @classmethod
    def select_answer(cls, question_id: str, option_index: int) -> "Action":
        return cls(action_type="select_answer", question_id=question_id, option_index=option_index)

    @classmethod
    def toggle_answer(cls, question_id: str, option_index: int) -> "Action":
        return cls(action_type="toggle_answer", question_id=question_id, option_index=option_index)

    @classmethod
    def submit_quiz(cls) -> "Action":
        return cls(action_type="submit_quiz")

    @classmethod
    def use_hint(cls, question_id: str) -> "Action":
        return cls(action_type="use_hint", question_id=question_id)

    @classmethod
    def retry_quiz(cls) -> "Action":
        return cls(action_type="retry_quiz")

    @classmethod
    def restart_task(cls) -> "Action":
        return cls(action_type="restart_task")


@dataclass
class State:
    """Full internal state for a course module episode."""

    task_id: str
    task_type: str
    difficulty: str
    title: str
    instruction: str
    phase: str = "study"
    sections: List[Dict[str, Any]] = field(default_factory=list)
    last_read_content: str = ""
    questions: List[Dict[str, Any]] = field(default_factory=list)
    quiz_answers: Dict[str, List[int]] = field(default_factory=dict)
    quiz_results: Optional[List[Dict[str, Any]]] = None
    hints_used: List[str] = field(default_factory=list)
    correct_answers: Dict[str, List[int]] = field(default_factory=dict)
    energy: int = 0
    energy_budget: int = 0
    steps_taken: int = 0
    step_budget: int = 0
    attempts: int = 0
    max_attempts: int = 3
    score: float = 0.0
    quiz_score: float = 0.0
    invalid_action_taken: bool = False
    last_feedback: str = "Ready to start."
    done: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Observation:
    """Agent-facing observation. Phase-aware and action-guiding."""

    phase: str
    task_type: str
    difficulty: str
    title: str
    instruction: str
    sections: List[Dict[str, Any]] = field(default_factory=list)
    current_content: str = ""
    questions: Optional[List[Dict[str, Any]]] = None
    energy_remaining: int = 0
    progress: str = ""
    available_actions: List[str] = field(default_factory=list)
    last_feedback: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
