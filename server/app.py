"""FastAPI wrapper for the upgraded WebTutor environment."""

from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional, Union
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict, Field
from server.environment import Action, WebTutorEnv

app = FastAPI(title="web_tutor_env", version="0.2.0",
    description="Multi-phase OpenEnv tutoring environment with study materials, quizzes, and energy management.")
env = WebTutorEnv(seed=42)

class ResetRequest(BaseModel):
    task_index: Optional[int] = Field(default=None, ge=0)

class StepRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"action_type": "read_section", "section_id": "s1"},
        {"action_type": "navigate", "target": "quiz"},
        {"action_type": "select_answer", "question_id": "q1", "option_index": 0},
        {"action_type": "toggle_answer", "question_id": "q3", "option_index": 1},
        {"action_type": "submit_quiz"},
        {"action_type": "use_hint", "question_id": "q1"},
        {"action_type": "retry_quiz"},
        {"action_type": "restart_task"},
    ]})
    action_type: Literal[
        "navigate", "read_section", "select_answer", "toggle_answer",
        "submit_quiz", "use_hint", "retry_quiz", "restart_task",
    ] = Field(..., description="The action to perform.")
    section_id: Optional[str] = Field(default=None, description="For read_section.")
    question_id: Optional[str] = Field(default=None, description="For select_answer, toggle_answer, use_hint.")
    option_index: Optional[int] = Field(default=None, description="For select_answer, toggle_answer.")
    target: Optional[str] = Field(default=None, description="For navigate: 'study' or 'quiz'.")

class ApiEnvelope(BaseModel):
    observation: Dict[str, Any]
    reward: float = Field(ge=0.0, le=1.0)
    done: bool
    info: Dict[str, Any]
    state: Dict[str, Any]

@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi.staticfiles import StaticFiles
import os

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.post("/reset")
def reset(request: ResetRequest):
    observation = env.reset(task_index=request.task_index)
    return ApiEnvelope(observation=observation, reward=0.0, done=False,
        info={"message": "Environment reset.", "task_index": env.current_task_index},
        state=env.state())

@app.post("/step")
def step(request: StepRequest):
    action_dict = {"action_type": request.action_type}
    if request.section_id is not None:
        action_dict["section_id"] = request.section_id
    if request.question_id is not None:
        action_dict["question_id"] = request.question_id
    if request.option_index is not None:
        action_dict["option_index"] = request.option_index
    if request.target is not None:
        action_dict["target"] = request.target
    observation, reward, done, info = env.step(action_dict)
    return ApiEnvelope(observation=observation, reward=float(reward), done=done, info=info, state=env.state())

@app.get("/state")
def get_state():
    state_data = env.state()
    return ApiEnvelope(observation=state_data, reward=0.0,
        done=bool(state_data.get("done", False)),
        info={"message": "Current state snapshot."}, state=state_data)

def create_app():
    return app