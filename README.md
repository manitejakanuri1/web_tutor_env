---
title: Web Tutor Environment
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

<div align="center">
  <h1>🧠 Web Tutor Environment</h1>
  <p><strong>A Premium Reinforcement Learning Playground built for the Meta PyTorch OpenEnv Hackathon</strong></p>
  
  <p>
    <a href="https://huggingface.co/spaces/Teja5454/web_tutor_env"><img src="https://img.shields.io/badge/Hugging%20Face-Space-blue?style=for-the-badge&logo=huggingface" alt="Hugging Face Space"></a>
    <a href="#"><img src="https://img.shields.io/badge/Status-Passing-success?style=for-the-badge" alt="Build Status"></a>
    <a href="#"><img src="https://img.shields.io/badge/UI-Premium-blueviolet?style=for-the-badge" alt="UI Premium"></a>
  </p>
</div>

Welcome to the **Web Tutor Environment**, a sophisticated multi-phase Reinforcement Learning playground. Instead of a standard backend-only API, this project features a **fully interactive, visually stunning Web Dashboard**, allowing Human Evaluators and Judges to manually play through the exact same logic that the AI Agent sees!

---

## 🚀 How to Test Manually (For Judges)

The environment has been entirely deployed on **Hugging Face Spaces**. You can explore the GUI immediately!

1. **Visit the Space:** Navigate to the root URL of this Hugging Face Space.
2. **Watch AI Play:** Click the animated 🤖 **Watch AI Play** button to sit back and watch a simulated LLM iteratively interact with the environment, navigating phases and taking quizzes.
3. **Or, Pick a Task Manually:** Use the Dropdown menu on the side to select a course difficulty (`HTML Basics [Easy]`, `REST APIs [Hard]`, etc.).
4. **Phase 1 (STUDY):** Click the reading materials on the left. The actual course content will render. **Manage your Energy Budget!** Every action costs energy.
5. **Phase 2 (QUIZ):** Answer questions based on the reading. We built custom handlers for Multi-Select scenarios.
6. **Phase 3 (REVIEW):** Submit the quiz. The environment will assign partial credit for multi-selects, grant an efficiency bonus, and provide explicit LLM pedagogical feedback on what you got wrong!

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
* **`static/`**: Houses the premium GUI that bridges human visibility to the AI backend, heavily enhanced with modern glassmorphism.

Good luck parsing, and enjoy the Web Tutor!
