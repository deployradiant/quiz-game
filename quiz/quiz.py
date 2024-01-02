import abc
from typing import Dict, List

class Quiz(abc.ABC):

    @abc.abstractmethod
    def generate_questions(self, number_of_questions: int) -> List[str]:
        pass

    @abc.abstractmethod
    def generate_answers(self, questions: List[str]) -> Dict[str, str]:
        pass