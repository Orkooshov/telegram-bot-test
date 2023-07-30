from database.entities import AnswerEntity, QuestionEntity, UserEntity#, UserAnswerEntity
from sqlalchemy.orm import Session


class UserOps:
    def insert(session: Session, user: UserEntity) -> None:
        existing_user = session.query(UserEntity).filter(
            UserEntity.username == user.username).first()
        if not existing_user:
            session.add(user)
            session.commit()

    def get_by_username(session: Session, username: str) -> UserEntity | None:
        return session.query(UserEntity).filter(UserEntity.username == username).first()


class QuestionOps:
    def get_all(session: Session) -> list[QuestionEntity]:
        return session.query(QuestionEntity).all()


class AnswerOps:
    def get_by_question(session: Session, question: QuestionEntity,
                        answer_text: str) -> AnswerEntity | None:
        return (session
                .query(AnswerEntity)
                .filter(AnswerEntity.question_id == question.id)
                .filter(AnswerEntity.text == answer_text).first())
    
    def insert(session: Session, answer: AnswerEntity) -> None:
        session.add(answer)
        session.commit()
