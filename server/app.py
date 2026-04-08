from fastapi import FastAPI
from pydantic import BaseModel
from server.healthcare_env_environment import HealthcareEnvironment
import uvicorn

app = FastAPI()

env = HealthcareEnvironment()


class ActionRequest(BaseModel):
    action: dict


@app.post("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(req: ActionRequest):
    return env.step(req.action)


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()