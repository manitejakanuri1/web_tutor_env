"""Smoke test for the upgraded web_tutor_env API."""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def pr(title, resp):
    print("\n>>> {}".format(title))
    print("Status: {}".format(resp.status_code))
    try:
        print(json.dumps(resp.json(), indent=2)[:1500])
    except Exception:
        print(resp.text[:500])


def main():
    print("=" * 70)
    print("WEB_TUTOR_ENV SMOKE TEST (v2 - Multi-Phase)")
    print("=" * 70)

    # 1. Health
    print("\n[1] GET /health")
    r = requests.get(BASE_URL + "/health")
    pr("Health", r)

    # 2. Reset
    print("\n[2] POST /reset (task 0)")
    r = requests.post(BASE_URL + "/reset", json={"task_index": 0})
    pr("Reset", r)
    obs = r.json().get("observation", {})

    # 3. State
    print("\n[3] GET /state")
    r = requests.get(BASE_URL + "/state")
    pr("State", r)

    # 4. Mini episode
    print("\n[4] Running multi-phase episode...")

    # Study phase: read sections
    for sec in obs.get("sections", []):
        sid = sec["section_id"]
        print("\n  Reading section: {}".format(sid))
        r = requests.post(BASE_URL + "/step", json={"action_type": "read_section", "section_id": sid})
        d = r.json()
        print("  Feedback: {}".format(d["observation"].get("last_feedback", "")[:200]))

    # Navigate to quiz
    print("\n  Navigating to quiz...")
    r = requests.post(BASE_URL + "/step", json={"action_type": "navigate", "target": "quiz"})
    d = r.json()
    obs = d["observation"]
    print("  Phase: {}".format(obs.get("phase")))

    # Answer questions
    questions = obs.get("questions", [])
    for q in questions:
        qid = q["question_id"]
        qtype = q.get("type", "single")
        if qtype == "multi":
            print("\n  Toggling option 0 for {} (multi)".format(qid))
            r = requests.post(BASE_URL + "/step", json={
                "action_type": "toggle_answer", "question_id": qid, "option_index": 0})
        else:
            print("\n  Selecting option 0 for {} (single)".format(qid))
            r = requests.post(BASE_URL + "/step", json={
                "action_type": "select_answer", "question_id": qid, "option_index": 0})
        print("  Feedback: {}".format(r.json()["observation"].get("last_feedback", "")[:200]))

    # Submit
    print("\n  Submitting quiz...")
    r = requests.post(BASE_URL + "/step", json={"action_type": "submit_quiz"})
    final = r.json()

    print("\n" + "=" * 70)
    print("EPISODE RESULTS")
    print("=" * 70)
    print("Reward: {}".format(final.get("reward")))
    print("Done: {}".format(final.get("done")))
    print("Feedback: {}".format(final["observation"].get("last_feedback", "")))
    print("Phase: {}".format(final["observation"].get("phase", "")))

    state = final.get("state", {})
    print("\nFinal state:")
    print("  Steps: {}/{}".format(state.get("steps_taken"), state.get("step_budget")))
    print("  Energy: {}/{}".format(state.get("energy"), state.get("energy_budget")))
    print("  Attempts: {}/{}".format(state.get("attempts"), state.get("max_attempts")))
    print("  Score: {}".format(state.get("score")))

    print("\n" + "=" * 70)
    print("SMOKE TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to", BASE_URL)
        print("Start: uvicorn server.app:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print("\nERROR: {}".format(e))
        import traceback
        traceback.print_exc()
