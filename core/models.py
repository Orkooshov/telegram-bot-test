from dataclasses import dataclass


@dataclass
class Question:
    title: str
    answers: list[str]
    id: int | None = None


@dataclass
class User:
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class UserAnswer:
    user: User
    question: Question
    answer_index: int

    @property
    def answer_text(self) -> str:
        return self.question.answers[self.answer_index]
