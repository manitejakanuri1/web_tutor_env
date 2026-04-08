"""Test script for the FastAPI server endpoints.

Run this script while the server is running on http://localhost:8000
"""

import json
import requests

BASE_URL = "http://localhost:8000"


def test_health():
    """Test GET /health"""
    print("\n" + "="*60)
    print("TEST 1: GET /health")
    print("="*60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    assert response.status_code == 200
    assert data["status"] == "ok"
    print("✓ PASS")


def test_reset():
    """Test POST /reset"""
    print("\n" + "="*60)
    print("TEST 2: POST /reset")
    print("="*60)
    response = requests.post(f"{BASE_URL}/reset", json={"task_index": 0})
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response keys: {list(data.keys())}")
    print(f"Observation: {json.dumps(data['observation'], indent=2)}")
    assert response.status_code == 200
    assert "observation" in data
    assert "state" in data
    assert data["observation"]["task_type"] == "mcq_quiz"
    print("✓ PASS")


def test_state():
    """Test GET /state"""
    print("\n" + "="*60)
    print("TEST 3: GET /state")
    print("="*60)
    response = requests.get(f"{BASE_URL}/state")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"State keys: {list(data.keys())}")
    print(f"Task type: {data['task_type']}")
    print(f"Difficulty: {data['difficulty']}")
    print(f"Steps taken: {data['steps_taken']}")
    print(f"Step budget: {data['step_budget']}")
    assert response.status_code == 200
    assert "task_type" in data
    assert "difficulty" in data
    print("✓ PASS")


def test_step_sequence():
    """Test POST /step with a full action sequence"""
    print("\n" + "="*60)
    print("TEST 4: POST /step - Full episode sequence")
    print("="*60)

    # Reset first
    requests.post(f"{BASE_URL}/reset", json={"task_index": 1})

    # Action 1: open_hint
    print("\n--- Step 1: open_hint ---")
    response = requests.post(
        f"{BASE_URL}/step",
        json={"action_type": "open_hint"}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Reward: {data['reward']}")
    print(f"Done: {data['done']}")
    print(f"Feedback: {data['observation']['last_feedback']}")
    assert response.status_code == 200
    assert isinstance(data["reward"], float)
    assert 0.0 <= data["reward"] <= 1.0, f"Reward {data['reward']} out of range [0, 1]"
    print("✓ Reward in valid range [0, 1]")

    # Action 2: select_option (correct answer)
    print("\n--- Step 2: select_option (index 2 = correct) ---")
    response = requests.post(
        f"{BASE_URL}/step",
        json={"action_type": "select_option", "option_index": 2}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Reward: {data['reward']}")
    print(f"Done: {data['done']}")
    print(f"Feedback: {data['observation']['last_feedback']}")
    assert response.status_code == 200
    assert isinstance(data["reward"], float)
    assert 0.0 <= data["reward"] <= 1.0, f"Reward {data['reward']} out of range [0, 1]"
    print("✓ Reward in valid range [0, 1]")

    # Action 3: submit
    print("\n--- Step 3: submit ---")
    response = requests.post(
        f"{BASE_URL}/step",
        json={"action_type": "submit"}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Reward: {data['reward']}")
    print(f"Done: {data['done']}")
    print(f"Feedback: {data['observation']['last_feedback']}")
    final_reward = data["reward"]
    assert response.status_code == 200
    assert isinstance(final_reward, float)
    assert 0.0 <= final_reward <= 1.0, f"Final reward {final_reward} out of range [0, 1]"
    print("✓ Reward in valid range [0, 1]")
    print(f"\n✓ FINAL REWARD: {final_reward} (PASS: correct answer + within budget + no invalid actions)")


def test_reward_bounds():
    """Test that rewards stay bounded in various scenarios"""
    print("\n" + "="*60)
    print("TEST 5: Reward bounds verification")
    print("="*60)

    # Scenario 1: Wrong answer
    print("\n--- Scenario 1: Wrong answer ---")
    requests.post(f"{BASE_URL}/reset", json={"task_index": 2})
    requests.post(f"{BASE_URL}/step", json={"action_type": "select_option", "option_index": 0})  # wrong
    response = requests.post(f"{BASE_URL}/step", json={"action_type": "submit"})
    reward = response.json()["reward"]
    print(f"Reward for wrong answer: {reward}")
    assert 0.0 <= reward <= 1.0
    assert reward == 0.0, "Wrong answer should give 0 reward"
    print("✓ PASS")

    # Scenario 2: Correct answer with steps over budget
    print("\n--- Scenario 2: Correct answer, steps over budget ---")
    requests.post(f"{BASE_URL}/reset", json={"task_index": 3})
    for _ in range(6):  # Go over step budget
        requests.post(f"{BASE_URL}/step", json={"action_type": "open_hint"})
    # This will cause invalid action after hint already used
    # Now select and submit
    requests.post(f"{BASE_URL}/step", json={"action_type": "select_option", "option_index": 1})
    response = requests.post(f"{BASE_URL}/step", json={"action_type": "submit"})
    reward = response.json()["reward"]
    print(f"Reward: {reward}")
    assert 0.0 <= reward <= 1.0
    print("✓ PASS")

    # Scenario 3: Clean episode
    print("\n--- Scenario 3: Perfect episode ---")
    requests.post(f"{BASE_URL}/reset", json={"task_index": 1})
    requests.post(f"{BASE_URL}/step", json={"action_type": "select_option", "option_index": 2})
    response = requests.post(f"{BASE_URL}/step", json={"action_type": "submit"})
    reward = response.json()["reward"]
    print(f"Reward: {reward}")
    assert 0.0 <= reward <= 1.0
    assert reward == 1.0, "Perfect episode should give max reward"
    print("✓ PASS")


def main():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# TESTING WEB_TUTOR_ENV API")
    print("#"*60)

    try:
        test_health()
        test_reset()
        test_state()
        test_step_sequence()
        test_reward_bounds()

        print("\n" + "#"*60)
        print("# ALL TESTS PASSED ✓")
        print("#"*60)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
