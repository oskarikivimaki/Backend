from pydantic import BaseModel

class Sensor(BaseModel):
    name: str
    status: dict
    values: dict
