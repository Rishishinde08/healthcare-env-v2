# from pydantic import BaseModel


# class HealthcareAction(BaseModel):
#     disease: str
#     hospital: str
#     urgency: str


# class HealthcareObservation(BaseModel):
#     result: str = ""
#     feedback: str = ""


from pydantic import BaseModel


class HealthcareAction(BaseModel):
    disease: str
    hospital: str
    urgency: str


class HealthcareObservation(BaseModel):
    observation: dict
    reward: float
    done: bool