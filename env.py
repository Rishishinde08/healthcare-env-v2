from server.healthcare_env_environment import HealthcareEnvironment


class HealthcareEnv:
    def __init__(self):
        self.env = HealthcareEnvironment()

    def reset(self):
        return self.env.reset()

    def step(self, action):
        return self.env.step(action)

    def state(self):
        return self.env.state


# IMPORTANT FIX
HealthcareEnv = HealthcareEnvironment