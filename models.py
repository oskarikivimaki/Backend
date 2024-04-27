from pydantic import BaseModel
from typing import Dict, List

class Sensor(BaseModel):
    name: str
    status: Dict[int, List[str]]
    values: dict
