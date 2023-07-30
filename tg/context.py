from dataclasses import dataclass

from core.models import Question


@dataclass
class PollContext:
    questions: list[Question]
    current_question_index: int

    @property
    def current_question(self) -> Question:
        return self.questions[self.current_question_index]

    @property
    def answered_all(self) -> bool:
        return self.current_question_index >= len(self.questions)
