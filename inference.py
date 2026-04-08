import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time

from env import HealthcareEnv

from openai import OpenAI



# =======================

# OpenAI Client (Required)

# =======================

try:

    client = OpenAI(

        base_url=os.getenv("API_BASE_URL"),

        api_key=os.getenv("HF_TOKEN")

    )

except Exception:

    client = None



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

    if isinstance(observation, dict):
     observation = observation.get("result", "")

    obs = observation.lower()



    if "fever" in obs or "cough" in obs:

        return {"disease": "flu", "hospital": "general", "urgency": "low"}



    elif "chest pain" in obs or "shortness of breath" in obs:

        return {"disease": "heart issue", "hospital": "cardiology", "urgency": "high"}



    elif "sugar" in obs or "blurred vision" in obs:

        return {"disease": "diabetes", "hospital": "endocrinologist", "urgency": "medium"}



    else:

        return {"disease": "general issue", "hospital": "general", "urgency": "low"}





# =======================

# MAIN (IMPORTANT FIX)

# =======================

def main():

    env = HealthcareEnv()



    log_start("healthcare", "healthcare_env", MODEL_NAME)



    obs = env.reset()

    rewards = []



    step = 1

    observation = obs["observation"]



    action = agent(observation)



    result = env.step(action)



    reward = result["reward"]

    done = result["done"]



    rewards.append(reward)



    log_step(step, action, reward, done)



    score = sum(rewards)

    success = score >= 0.7



    log_end(success, step, score, rewards)





# =======================

# ENTRY POINT FIX 🔥

# =======================

if __name__ == "__main__":

    main()



    # Keep container alive

    while True:

        time.sleep(60)