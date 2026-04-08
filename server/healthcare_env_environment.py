from uuid import uuid4
import random

# =======================
# DUMMY BASE CLASSES
# =======================
class Environment:
    pass


class State:
    def __init__(self, episode_id, step_count):
        self.episode_id = episode_id
        self.step_count = step_count


# =======================
# TASK IMPORTS
# =======================
from tasks.easy import TASKS as EASY_TASKS
from tasks.medium import TASKS as MEDIUM_TASKS
from tasks.hard import TASKS as HARD_TASKS


class HealthcareEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.tasks = EASY_TASKS + MEDIUM_TASKS + HARD_TASKS
        self.current_task = None

    # =======================
    # RESET
    # =======================
    def reset(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        if not self.tasks:
            return {
                "observation": {"result": "No tasks", "feedback": "Error"},
                "reward": 0.0,
                "done": True
            }

        self.current_task = random.choice(self.tasks)

        return {
            "observation": {
                "result": str(self.current_task["input"]),
                "feedback": "New healthcare task loaded"
            },
            "reward": 0.0,
            "done": False
        }

    # =======================
    # STEP
    # =======================
    def step(self, action):
        self._state.step_count += 1

        if self.current_task is None:
            return {
                "observation": {
                    "result": "No task",
                    "feedback": "Reset required"
                },
                "reward": 0.0,
                "done": True
            }

        expected = self.current_task["expected"]

        reward = 0.0
        feedback = []

        if action.get("disease") == expected["disease"]:
            reward += 0.4
            feedback.append("disease correct")

        if action.get("hospital") == expected["hospital"]:
            reward += 0.3
            feedback.append("hospital correct")

        if action.get("urgency") == expected["urgency"]:
            reward += 0.3
            feedback.append("urgency correct")

        return {
            "observation": {
                "result": str(self.current_task["input"]),
                "feedback": ", ".join(feedback)
            },
            "reward": float(reward),
            "done": True
        }

    # =======================
    # STATE
    # =======================
    @property
    def state(self):
        return {
            "episode_id": self._state.episode_id,
            "step_count": self._state.step_count
        }