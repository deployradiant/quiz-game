import abc
from typing import Dict, List

class Quiz(abc.ABC):

    @abc.abstractmethod
    def generate_questions(self, number_of_questions: int) -> List[str]:
        pass

    @abc.abstractmethod
    def check_answers(self, questions_with_answers: List[str]) -> Dict[str, str]:
        pass