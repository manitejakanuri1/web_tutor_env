# 2-Minute Demo Script for web_tutor_env

## 0:00-0:15 | What to say first

Hi, this is web_tutor_env, a hackathon-ready OpenEnv-style reinforcement learning environment.
It simulates realistic tutoring tasks where an agent reads instructions, can use hints, selects an answer, and submits.

## 0:15-0:30 | What to open

Open these in browser:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

Say:

This is the FastAPI app and Swagger UI where I can test the environment live.

## 0:30-1:15 | What to click in Swagger UI

In Swagger UI, show these endpoints in order:

1. GET /health
- Click Try it out
- Click Execute
- Say: This confirms the server is healthy.

2. POST /reset
- Click Try it out
- Use body:
  {
    "task_index": 0
  }
- Click Execute
- Say: This starts a new episode and returns observation plus full state.

3. GET /state
- Click Try it out
- Click Execute
- Say: This shows the current internal environment state.

4. POST /step (open_hint)
- Click Try it out
- Use body:
  {
    "action_type": "open_hint"
  }
- Click Execute

5. POST /step (select_option)
- Click Try it out
- Use body:
  {
    "action_type": "select_option",
    "option_index": 0
  }
- Click Execute

6. POST /step (submit)
- Click Try it out
- Use body:
  {
    "action_type": "submit"
  }
- Click Execute
- Say: Here we get reward, done flag, info, and final state.

## 1:15-1:35 | What to show in terminal

Show terminal commands:

python smoke_test.py

Optional:

python test_api.py

Say:

These scripts run endpoint checks and full mini-episodes automatically.

## 1:35-1:50 | How to explain reward logic

Say:

Reward is always between 0 and 1.
Correct final completion gives 0.7.
If the agent stays within step budget, it gets up to 0.2.
If no invalid actions are taken, it gets 0.1.
Wrong final answer gives 0.0.
Hints are allowed, but efficiency reward can be reduced.

## 1:50-2:00 | Why this is a real-world RL environment

Say:

This is realistic because agents must make multi-step decisions, handle optional hints, avoid invalid actions, and optimize both correctness and efficiency.
So it is useful for training and evaluating practical assistant behavior, not just toy RL tasks.

## Closing line

Thanks for watching. This project is lightweight, locally runnable, Docker-ready, and designed for quick OpenEnv-style experimentation.
