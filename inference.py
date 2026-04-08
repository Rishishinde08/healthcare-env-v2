import os
import sys
import time

# 🔥 FORCE ROOT PATH (VERY IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# 🔥 SAFE IMPORT (FINAL FIX)
try:
    from env import HealthcareEnv
except Exception as e:
    print("IMPORT ERROR:", str(e))
    raise e


# =======================
# CONFIG
# =======================
MODEL_NAME = os.getenv("MODEL_NAME", "dummy-model")


# =======================
# Logging Functions
# =======================
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}")


def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")


def log_end(success, steps, score, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


# =======================
# Agent Logic
# =======================
def agent(observation):
    try:
        if isinstance(observation, dict):
            observation = observation.get("result", "")

        obs = str(observation).lower()

        if "fever" in obs or "cough" in obs:
            return {"disease": "flu", "hospital": "general", "urgency": "low"}

        elif "chest" in obs or "breath" in obs:
            return {"disease": "heart issue", "hospital": "cardiology", "urgency": "high"}

        elif "sugar" in obs or "vision" in obs:
            return {"disease": "diabetes", "hospital": "endocrinologist", "urgency": "medium"}

        else:
            return {"disease": "general issue", "hospital": "general", "urgency": "low"}

    except Exception as e:
        print("AGENT ERROR:", str(e))
        return {"disease": "general issue", "hospital": "general", "urgency": "low"}


# =======================
# MAIN
# =======================
def main():
    try:
        env = HealthcareEnv()

        log_start("healthcare", "healthcare_env", MODEL_NAME)

        obs = env.reset()
        rewards = []

        step = 1

        # 🔥 SAFE extraction
        observation = obs.get("observation", {})

        action = agent(observation)

        result = env.step(action)

        reward = float(result.get("reward", 0))
        done = bool(result.get("done", False))

        rewards.append(reward)

        log_step(step, action, reward, done)

        score = sum(rewards)
        success = score >= 0.7

        log_end(success, step, score, rewards)

    except Exception as e:
        print("MAIN ERROR:", str(e))


# =======================
# ENTRY POINT
# =======================
if __name__ == "__main__":
    main()

    # keep container alive
    while True:
        time.sleep(60)