"""Baseline inference script for web_tutor_env.

Uses OpenAI client + deterministic fallback to navigate the multi-phase environment.
Emits [START], [STEP], [END] logs for hackathon evaluation.
"""

import os
import json
from openai import OpenAI
from client import WebTutorClient

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.environ.get("HF_TOKEN")
api_key = HF_TOKEN or os.environ.get("OPENAI_API_KEY", "dummy-key")

llm_client = OpenAI(base_url=API_BASE_URL, api_key=api_key)

SYSTEM_PROMPT = """You are an AI agent on a tutoring platform.
Phases: study -> quiz -> review.
In STUDY: read sections. In QUIZ: answer questions. In REVIEW: retry.

Actions (respond with ONLY valid JSON):
{"action_type": "read_section", "section_id": "s1"}
{"action_type": "navigate", "target": "quiz"}
{"action_type": "navigate", "target": "study"}
{"action_type": "select_answer", "question_id": "q1", "option_index": 0}
{"action_type": "toggle_answer", "question_id": "q1", "option_index": 0}
{"action_type": "submit_quiz"}
{"action_type": "use_hint", "question_id": "q1"}
{"action_type": "retry_quiz"}

Strategy: Read ALL sections first, navigate to quiz, answer all questions, submit.
For multi-select: use toggle_answer for EACH correct option.
RESPOND WITH ONLY JSON."""


def get_llm_action(observation):
    try:
        response = llm_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "State:\n" + json.dumps(observation, indent=2)},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return None


def get_fallback_action(observation):
    phase = observation.get("phase", "study")
    sections = observation.get("sections", [])
    questions = observation.get("questions") or []

    if phase == "study":
        for sec in sections:
            if not sec.get("read", False):
                return {"action_type": "read_section", "section_id": sec["section_id"]}
        return {"action_type": "navigate", "target": "quiz"}

    elif phase == "quiz":
        for q in questions:
            qid = q["question_id"]
            current = q.get("your_answer", [])
            if len(current) == 0:
                if q.get("type") == "multi":
                    return {"action_type": "toggle_answer", "question_id": qid, "option_index": 0}
                else:
                    return {"action_type": "select_answer", "question_id": qid, "option_index": 0}
        return {"action_type": "submit_quiz"}

    elif phase == "review":
        return {"action_type": "retry_quiz"}

    return {"action_type": "restart_task"}


def run_episode(env_client, task_index):
    try:
        observation = env_client.reset(task_index=task_index)
        state = env_client.state()
        task_name = state.get("task_id", f"task_{task_index}")
    except Exception:
        task_name = f"task_{task_index}"

    print(f"[START] task={task_name} env=web_tutor_env model={MODEL_NAME}", flush=True)

    done = False
    step_count = 0
    rewards = []
    score = 0.0
    error = "null"

    while not done and step_count < 50:
        action = get_llm_action(observation)
        if action is None:
            action = get_fallback_action(observation)

        action_str = json.dumps(action).replace('"', "'")

        try:
            observation, reward, done, info = env_client.step(action)
            error = "null"
        except Exception as e:
            reward = 0.0
            done = True
            error = str(e).replace('"', "'")

        step_count += 1
        rewards.append(reward)
        done_val = str(done).lower()

        print(f"[STEP]  step={step_count} action={action_str} reward={reward:.2f} done={done_val} error={error}", flush=True)
        
        if done:
            state = env_client.state()
            score = state.get("score", reward)
            break

    success_val = str(score > 0.5).lower()
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    if not rewards:
        rewards_str = "0.00"

    print(f"[END]   success={success_val} steps={step_count} score={score:.3f} rewards={rewards_str}", flush=True)
    return score


def main():
    env_client = WebTutorClient(seed=42)
    num_tasks = min(5, len(env_client.env.task_bank))
    total = 0.0

    print("=== web_tutor_env inference ===")
    print("Model: {}".format(MODEL_NAME))
    print("Tasks: {}".format(num_tasks))
    print()

    for i in range(num_tasks):
        total += run_episode(env_client, i)
        print()

    print("=== Summary ===")
    print("Total: {:.4f}  Average: {:.4f}".format(total, total / num_tasks))


if __name__ == "__main__":
    main()
