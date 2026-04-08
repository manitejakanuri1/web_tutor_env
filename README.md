---
title: Web Tutor Env
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🧠 Web Tutor Environment

Welcome to the **Web Tutor Environment**, a sophisticated multi-phase Reinforcement Learning playground built specifically for the **Meta PyTorch OpenEnv Hackathon**.

Instead of a standard backend-only API, this project features a **fully interactive, visually stunning Web Dashboard**, allowing Human Evaluators and Judges to manually play through the exact same logic that the AI Agent sees!

---

## 🚀 How to Test Manually (For Judges)

The environment has been entirely deployed on **Hugging Face Spaces**. You can explore the GUI immediately!

1. **Visit the Space:** Simply navigate to the root URL of this Hugging Face Space.
2. **Dynamic UI:** You will be greeted by a dark-mode, responsive Web Dashboard!
3. **Pick a Task:** Use the Dropdown menu on the bottom-left sidebar to explicitly select a course difficulty (`HTML Basics [Easy]`, `REST APIs [Hard]`, etc.), or leave it on `Random Task`.
4. **Click "Restart Episode":** This initializes the internal state engine.
5. **Phase 1 (STUDY):** Click the reading materials on the left. The actual course content will render. **Manage your Energy Budget!** Every action costs energy.
6. **Phase 2 (QUIZ):** Click **"Go to Quiz"**. You must answer questions based on the reading. We built custom handlers for Multi-Select scenarios (where you must toggle multiple answers).
7. **Phase 3 (REVIEW):** Click the **Submit** button. The environment will assign partial credit for multi-selects, grant an efficiency bonus, and provide explicit LLM pedagogical feedback on what you got wrong!

---

## 🤖 How the Agent Operates (Technical Details)

This environment rigidly adheres to the `openenv-core` criteria required by the hackathon.

### Multi-Phase Flow
The environment uses a State Machine built into `server/environment.py`:
`[STUDY] -> [QUIZ] -> [REVIEW] -> [COMPLETED]`

### Actions Space
The Agent can emit standard JSON dictionary actions directly to `POST /step`:
* `{"action_type": "read_section", "section_id": "s1"}` (Costs 1 Energy)
* `{"action_type": "navigate", "target": "quiz"}` 
* `{"action_type": "select_answer", "question_id": "q1", "option_index": 0}` 
* `{"action_type": "toggle_answer"}` (For Multi-select parsing)
* `{"action_type": "use_hint"}` (Costs 2 Energy)
* `{"action_type": "submit_quiz"}`

### Evaluation Compliance Output
We heavily engineered `inference.py` to seamlessly execute evaluation loops. 
* It intercepts the OpenAI client (or Hugging Face routing).
* It gracefully parses the `[START]`, `[STEP]`, and `[END]` logging syntax required by the Hackathon automated regex parsers.
* Environmental variables (`API_BASE_URL`, `MODEL_NAME`, `HF_TOKEN`) are flawlessly bound.

---

## 🛠 Project Architecture

* **`server/app.py`**: A FastAPI backend that hosts both the JSON API for the LLMs `(/step, /reset, /state)`, and silently mounts our interactive Vanilla JS web facade.
* **`server/environment.py`**: The core RL engine. Tracks attempts, calculates step budgets, drops validation errors if agents hallucinate, and manages partial reward algorithms.
* **`models.py` & `tasks.py`**: Stores the structured task dictionary and Python Typed DataClasses. 
* **`static/`**: Houses the premium GUI that bridges human visibility to the AI backend.

Good luck parsing, and enjoy the Web Tutor!
