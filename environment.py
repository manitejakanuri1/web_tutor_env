"""Multi-phase OpenEnv-style tutoring environment.

The agent navigates: study -> quiz -> review -> (retry or completed)

Key features:
- Information retrieval: agent must read study materials to find answers
- Energy management: each action costs energy
- Multi-select questions: some require selecting multiple correct answers
- Multi-attempt: wrong submissions allow retry with reduced max reward
- Dense feedback: wrong answers produce pedagogical hints
"""

from __future__ import annotations
import copy
import random
from typing import Any, Dict, List, Optional, Tuple, Union

from models import Action, Observation, State
from tasks import get_task_bank

ENERGY_COST = {
    "navigate": 0,
    "read_section": 1,
    "select_answer": 0,
    "toggle_answer": 0,
    "submit_quiz": 1,
    "use_hint": 2,
    "retry_quiz": 1,
    "restart_task": 0,
}


class WebTutorEnv:
    """Multi-phase tutoring environment with study materials and quizzes."""

    def __init__(self, seed: Optional[int] = None):
        self.random = random.Random(seed)
        self.task_bank = get_task_bank()
        self.current_task_index: int = -1
        self._state: Optional[State] = None
        self._task_data: Optional[Dict[str, Any]] = None

    def reset(self, task_index: Optional[int] = None) -> Dict[str, Any]:
        """Start a new episode and return the initial observation."""
        if task_index is None:
            task_index = self.random.randrange(len(self.task_bank))
        else:
            task_index = task_index % len(self.task_bank)

        self.current_task_index = task_index
        task = copy.deepcopy(self.task_bank[task_index])
        self._task_data = task

        sections = []
        for mat in task["study_materials"]:
            sections.append({
                "section_id": mat["section_id"],
                "title": mat["title"],
                "read": False,
            })

        questions = []
        correct_answers = {}
        for q in task["quiz"]:
            questions.append({
                "question_id": q["question_id"],
                "question": q["question"],
                "options": list(q["options"]),
                "type": q["type"],
            })
            correct_answers[q["question_id"]] = list(q["correct_options"])

        self._state = State(
            task_id=task["id"],
            task_type=task["task_type"],
            difficulty=task["difficulty"],
            title=task["title"],
            instruction=task["instruction"],
            phase="study",
            sections=sections,
            questions=questions,
            correct_answers=correct_answers,
            energy=task["energy_budget"],
            energy_budget=task["energy_budget"],
            step_budget=task["step_budget"],
            max_attempts=task.get("max_attempts", 3),
            last_feedback=(
                "Episode started. You are in the STUDY phase. "
                "Read study materials, then navigate to quiz."
            ),
        )
        return self._make_observation().to_dict()

    def step(self, action: Union[Action, Dict[str, Any], str]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """Apply one action. Returns (observation, reward, done, info)."""
        if self._state is None:
            raise RuntimeError("Call reset() before step().")

        try:
            parsed = self._parse_action(action)
        except Exception:
            self._mark_invalid("Malformed action payload.")
            return self._make_observation().to_dict(), 0.0, False, self._info()

        reward = 0.0
        done = False

        if self._state.done:
            if parsed.action_type == "restart_task":
                return self._do_restart()
            return self._make_observation().to_dict(), 0.0, True, self._info()

        cost = ENERGY_COST.get(parsed.action_type, 1)
        if cost > 0 and self._state.energy < cost:
            self._mark_invalid(
                "Not enough energy for '{}' (need {}, have {}). Submit or restart.".format(
                    parsed.action_type, cost, self._state.energy))
            self._state.steps_taken += 1
            return self._make_observation().to_dict(), 0.0, False, self._info()

        self._state.energy -= cost
        self._state.steps_taken += 1

        if parsed.action_type == "navigate":
            self._handle_navigate(parsed.target)
        elif parsed.action_type == "read_section":
            self._handle_read_section(parsed.section_id)
        elif parsed.action_type == "select_answer":
            self._handle_select_answer(parsed.question_id, parsed.option_index)
        elif parsed.action_type == "toggle_answer":
            self._handle_toggle_answer(parsed.question_id, parsed.option_index)
        elif parsed.action_type == "submit_quiz":
            reward, done = self._handle_submit_quiz()
        elif parsed.action_type == "use_hint":
            self._handle_use_hint(parsed.question_id)
        elif parsed.action_type == "retry_quiz":
            self._handle_retry_quiz()
        elif parsed.action_type == "restart_task":
            return self._do_restart()
        else:
            self._state.energy += cost
            self._mark_invalid("Unknown action_type: '{}'".format(parsed.action_type))

        if not self._state.done and self._state.steps_taken >= self._state.step_budget:
            self._state.done = True
            self._state.phase = "completed"
            self._state.last_feedback = "Step budget exhausted. Final score: {:.2f}".format(self._state.score)
            done = True

        return self._make_observation().to_dict(), reward, done, self._info()

    def state(self) -> Dict[str, Any]:
        """Return full internal state as dictionary."""
        if self._state is None:
            return {}
        return self._state.to_dict()

    # ── Action Handlers ──────────────────────────────────────────────────

    def _handle_navigate(self, target):
        s = self._state
        if target == "quiz":
            if s.phase == "study":
                s.phase = "quiz"
                s.last_feedback = "Navigated to QUIZ phase. Answer questions and submit."
            elif s.phase == "quiz":
                s.last_feedback = "Already in quiz phase."
            else:
                self._mark_invalid("Cannot navigate to quiz from current phase.")
        elif target == "study":
            if s.phase in ("quiz", "review"):
                s.phase = "study"
                s.last_feedback = "Returned to STUDY phase."
            elif s.phase == "study":
                s.last_feedback = "Already in study phase."
            else:
                self._mark_invalid("Cannot navigate to study from current phase.")
        else:
            self._mark_invalid("Invalid target: '{}'. Use 'study' or 'quiz'.".format(target))

    def _handle_read_section(self, section_id):
        s = self._state
        if s.phase != "study":
            self._mark_invalid("Can only read sections in STUDY phase.")
            return
        if not section_id:
            self._mark_invalid("read_section requires section_id.")
            return

        section = None
        for sec in s.sections:
            if sec["section_id"] == section_id:
                section = sec
                break

        if section is None:
            self._mark_invalid("Section '{}' not found.".format(section_id))
            return

        if section["read"]:
            s.last_feedback = "Section '{}' already read.".format(section["title"])
            s.energy += ENERGY_COST["read_section"]
        else:
            section["read"] = True
            content = ""
            for mat in self._task_data["study_materials"]:
                if mat["section_id"] == section_id:
                    content = mat["content"]
                    break
            s.last_read_content = content
            s.last_feedback = "Section '{}' read. Content: {}".format(section["title"], content)

    def _handle_select_answer(self, question_id, option_index):
        s = self._state
        if s.phase != "quiz":
            self._mark_invalid("Can only answer in QUIZ phase.")
            return
        if not question_id or option_index is None:
            self._mark_invalid("select_answer requires question_id and option_index.")
            return

        q = self._find_question(question_id)
        if q is None:
            return

        if not isinstance(option_index, int) or option_index < 0 or option_index >= len(q["options"]):
            self._mark_invalid("option_index {} out of range.".format(option_index))
            return

        s.quiz_answers[question_id] = [option_index]
        s.last_feedback = "Selected option {} ('{}') for {}.".format(
            option_index, q["options"][option_index], question_id)

    def _handle_toggle_answer(self, question_id, option_index):
        s = self._state
        if s.phase != "quiz":
            self._mark_invalid("Can only toggle in QUIZ phase.")
            return
        if not question_id or option_index is None:
            self._mark_invalid("toggle_answer requires question_id and option_index.")
            return

        q = self._find_question(question_id)
        if q is None:
            return

        if not isinstance(option_index, int) or option_index < 0 or option_index >= len(q["options"]):
            self._mark_invalid("option_index {} out of range.".format(option_index))
            return

        current = s.quiz_answers.get(question_id, [])
        if option_index in current:
            current.remove(option_index)
        else:
            current.append(option_index)
        s.quiz_answers[question_id] = sorted(current)
        s.last_feedback = "Toggled option {} for {}. Current: {}".format(
            option_index, question_id, s.quiz_answers[question_id])

    def _handle_submit_quiz(self):
        s = self._state
        if s.phase != "quiz":
            self._mark_invalid("Can only submit in QUIZ phase.")
            return 0.0, False

        unanswered = [q["question_id"] for q in s.questions
                      if q["question_id"] not in s.quiz_answers or not s.quiz_answers[q["question_id"]]]
        if unanswered:
            self._mark_invalid("Unanswered questions: {}".format(unanswered))
            s.energy += ENERGY_COST["submit_quiz"]
            return 0.0, False

        s.attempts += 1
        results = []
        correct_count = 0.0

        for q in s.questions:
            qid = q["question_id"]
            selected = sorted(s.quiz_answers.get(qid, []))
            correct = sorted(s.correct_answers[qid])
            is_correct = selected == correct

            if q["type"] == "multi":
                cs = set(correct)
                ss = set(selected)
                tp = len(cs & ss)
                fp = len(ss - cs)
                fn = len(cs - ss)
                if tp == 0:
                    partial = 0.0
                else:
                    prec = tp / (tp + fp)
                    rec = tp / (tp + fn)
                    partial = 2 * prec * rec / (prec + rec)
            else:
                partial = 1.0 if is_correct else 0.0

            correct_count += partial

            task_q = None
            for tq in self._task_data["quiz"]:
                if tq["question_id"] == qid:
                    task_q = tq
                    break

            feedback = "Correct!" if is_correct else "Wrong. {}".format(task_q["wrong_feedback"])
            results.append({
                "question_id": qid,
                "correct": is_correct,
                "partial_score": round(partial, 2),
                "your_answer": selected,
                "feedback": feedback,
            })

        s.quiz_results = results
        quiz_score = correct_count / len(s.questions) if s.questions else 0.0
        reward = self._compute_reward(quiz_score)
        s.score = reward

        all_correct = all(r["correct"] for r in results)

        if all_correct:
            s.phase = "completed"
            s.done = True
            s.last_feedback = "All correct! Reward: {:.2f}".format(reward)
        elif s.attempts >= s.max_attempts:
            s.phase = "completed"
            s.done = True
            s.last_feedback = "Max attempts reached. Reward: {:.2f}, Score: {:.0%}".format(reward, quiz_score)
        else:
            s.phase = "review"
            s.last_feedback = "Attempt {}/{}. Score: {:.0%}. Review and retry.".format(
                s.attempts, s.max_attempts, quiz_score)

        return reward, s.done

    def _handle_use_hint(self, question_id):
        s = self._state
        if s.phase not in ("quiz", "study"):
            self._mark_invalid("Hints only in study or quiz phase.")
            return
        if not question_id:
            self._mark_invalid("use_hint requires question_id.")
            return
        if question_id in s.hints_used:
            s.last_feedback = "Hint for '{}' already used.".format(question_id)
            s.energy += ENERGY_COST["use_hint"]
            return

        task_q = None
        for tq in self._task_data["quiz"]:
            if tq["question_id"] == question_id:
                task_q = tq
                break
        if task_q is None:
            self._mark_invalid("Question '{}' not found.".format(question_id))
            s.energy += ENERGY_COST["use_hint"]
            return

        s.hints_used.append(question_id)
        s.last_feedback = "Hint for {}: Answer is in section '{}'.".format(
            question_id, task_q.get("key_section", ""))

    def _handle_retry_quiz(self):
        s = self._state
        if s.phase != "review":
            self._mark_invalid("Can only retry from REVIEW phase.")
            return
        if s.attempts >= s.max_attempts:
            self._mark_invalid("No attempts remaining.")
            return
        s.quiz_answers = {}
        s.quiz_results = None
        s.phase = "quiz"
        s.last_feedback = "Retry started (attempt {}/{}).".format(s.attempts + 1, s.max_attempts)

    # ── Reward ───────────────────────────────────────────────────────────

    def _compute_reward(self, quiz_score: float) -> float:
        """Reward in [0.0, 1.0]: correctness(0.6) + efficiency(0.2) + clean(0.1) + attempt(0.1)"""
        s = self._state
        correctness = 0.6 * quiz_score
        step_eff = max(0, 1 - s.steps_taken / s.step_budget) if s.step_budget > 0 else 0
        energy_eff = s.energy / s.energy_budget if s.energy_budget > 0 else 0
        efficiency = 0.2 * (step_eff + energy_eff) / 2
        clean = 0.1 if not s.invalid_action_taken else 0.0
        attempt_bonus = 0.1 if s.attempts <= 1 else (0.05 if s.attempts == 2 else 0.0)
        total = correctness + efficiency + clean + attempt_bonus
        return round(max(0.0, min(1.0, total)), 4)

    # ── Observation ──────────────────────────────────────────────────────

    def _make_observation(self) -> Observation:
        s = self._state
        sections_view = [{"section_id": sec["section_id"], "title": sec["title"], "read": sec["read"]} for sec in s.sections]

        questions_view = None
        if s.phase in ("quiz", "review"):
            questions_view = []
            for q in s.questions:
                qid = q["question_id"]
                qv = {
                    "question_id": qid,
                    "question": q["question"],
                    "options": q["options"],
                    "type": q["type"],
                    "your_answer": s.quiz_answers.get(qid, []),
                }
                if s.phase == "review" and s.quiz_results:
                    for r in s.quiz_results:
                        if r["question_id"] == qid:
                            qv["correct"] = r["correct"]
                            qv["feedback"] = r["feedback"]
                            qv["partial_score"] = r["partial_score"]
                            break
                questions_view.append(qv)

        available = self._available_actions()
        progress = "{}/{} steps | {}/{} energy | attempt {}/{}".format(
            s.steps_taken, s.step_budget, s.energy, s.energy_budget, s.attempts, s.max_attempts)

        return Observation(
            phase=s.phase, task_type=s.task_type, difficulty=s.difficulty,
            title=s.title, instruction=s.instruction, sections=sections_view,
            current_content=s.last_read_content, questions=questions_view,
            energy_remaining=s.energy, progress=progress,
            available_actions=available, last_feedback=s.last_feedback,
        )

    def _available_actions(self) -> List[str]:
        s = self._state
        if s.done:
            return ["restart_task"]
        actions = ["restart_task"]
        if s.phase == "study":
            actions.extend(["read_section", "navigate(quiz)"])
            if s.energy >= ENERGY_COST["use_hint"]:
                actions.append("use_hint")
        elif s.phase == "quiz":
            actions.extend(["select_answer", "toggle_answer", "navigate(study)"])
            if s.energy >= ENERGY_COST["submit_quiz"]:
                actions.append("submit_quiz")
            if s.energy >= ENERGY_COST["use_hint"]:
                actions.append("use_hint")
        elif s.phase == "review":
            if s.attempts < s.max_attempts:
                actions.extend(["retry_quiz", "navigate(study)"])
        return actions

    # ── Helpers ───────────────────────────────────────────────────────────

    def _find_question(self, question_id):
        for q in self._state.questions:
            if q["question_id"] == question_id:
                return q
        self._mark_invalid("Question '{}' not found.".format(question_id))
        return None

    def _parse_action(self, action):
        if isinstance(action, Action):
            return action
        if isinstance(action, str):
            return Action(action_type=action)
        if isinstance(action, dict):
            return Action(
                action_type=str(action.get("action_type", "")),
                section_id=action.get("section_id"),
                question_id=action.get("question_id"),
                option_index=action.get("option_index"),
                target=action.get("target"),
            )
        raise TypeError("Action must be Action, dict, or string.")

    def _do_restart(self):
        obs = self.reset(task_index=self.current_task_index)
        return obs, 0.0, False, self._info()

    def _mark_invalid(self, message):
        self._state.invalid_action_taken = True
        self._state.last_feedback = "Invalid action: {}".format(message)

    def _info(self):
        return {"state": self._state.to_dict(), "task_index": self.current_task_index}
