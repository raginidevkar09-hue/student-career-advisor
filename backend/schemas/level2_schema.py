from pydantic import BaseModel
from typing import Dict

class Level2Submission(BaseModel):
    student_id: str
    answers: Dict[str, int]
