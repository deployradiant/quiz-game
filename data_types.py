from pydantic import BaseModel


class Questions(BaseModel):
    questions: list[str]


class Answer(BaseModel):
    is_correct: bool
    correct_answer: str
