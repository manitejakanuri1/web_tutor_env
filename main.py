"""Minimal demo for web_tutor_env.

This script runs one complete episode so you can see the environment API in
action without needing any extra framework.
"""

from __future__ import annotations

from environment import WebTutorEnv
from models import Action


def run_demo_episode() -> None:
    env = WebTutorEnv(seed=42)

    # Pick a fixed task so the demo is reproducible.
    observation = env.reset(task_index=1)
    print("Initial observation:")
    print(observation)
    print()

    done = False
    total_reward = 0.0

    # A simple scripted policy: use the hint if it exists, then submit the
    # known correct option for the chosen task.
    if observation["hint_available"]:
        observation, reward, done, info = env.step(Action.open_hint())
        total_reward += reward
        print("After open_hint:")
        print(observation)
        print("reward:", reward)
        print("done:", done)
        print("info:", info)
        print()

    state = env.state()
    correct_index = state["correct_option_index"]
    observation, reward, done, info = env.step(Action.select_option(correct_index))
    total_reward += reward
    print("After select_option:")
    print(observation)
    print("reward:", reward)
    print("done:", done)
    print("info:", info)
    print()

    observation, reward, done, info = env.step(Action.submit())
    total_reward += reward
    print("After submit:")
    print(observation)
    print("reward:", reward)
    print("done:", done)
    print("info:", info)
    print()

    print("Episode finished.")
    print("Total reward:", total_reward)


if __name__ == "__main__":
    run_demo_episode()
