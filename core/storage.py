from database.entities import AnswerEntity, QuestionEntity, UserEntity
from database.connection import engine
from sqlalchemy.orm import Session
from core.models import Question, UserAnswer, User
from database.operations import AnswerOps, UserOps


class UserStorage:
    def model_to_entity(model: User) -> UserEntity:
        return UserEntity(id=model.id, username=model.username,
                          first_name=model.first_name, last_name=model.last_name)

    def entity_to_model(entity: UserEntity) -> User:
        return User(id=entity.id, username=entity.username,
                    first_name=entity.first_name, last_name=entity.last_name)

    @classmethod
    def insert(cls, user: User) -> None:
        with Session(engine) as db:
            UserOps.insert(db, cls.model_to_entity(user))

    @classmethod
    def get_by_username(cls, username: str) -> User | None:
        with Session(engine) as db:
            user_entity = UserOps.get_by_username(db, username)
            return cls.entity_to_model(user_entity)


class QuestionStorage:
    def entity_to_model(entity: QuestionEntity) -> Question:
        return Question(title=entity.title,
                        answers=[i.text for i in entity.answers],
                        id=entity.id)

    def model_to_entity(model: Question) -> QuestionEntity:
        answers = [AnswerEntity(question_id=model.id, text=i)
                   for i in model.answers]
        return QuestionEntity(id=model.id, title=model.title, answers=answers)

    @classmethod
    def get_all(cls) -> list[Question]:
        with Session(engine) as db:
            return [cls.entity_to_model(i)
                    for i in db.query(QuestionEntity).all()]

    @classmethod
    def insert(cls, question: Question) -> None:
        with Session(engine) as db:
            db.add(cls.model_to_entity(question))
            db.commit()


class UserAnswerStorage:
    def entity_to_model(answer: AnswerEntity, user: User) -> UserAnswer:
        question = QuestionStorage.entity_to_model(answer.question)
        answer_index = question.answers.index(answer.text)
        return UserAnswer(user=user, question=question, answer_index=answer_index)

    @classmethod
    def insert(cls, ua: UserAnswer) -> None:
        with Session(engine) as db:
            user_entity = db.query(UserEntity).filter(
                UserEntity.id == ua.user.id).first()
            # user = ua.user
            answer = AnswerOps.get_by_question(db, ua.question, ua.answer_text)
            user_entity.answers.append(answer)
            db.commit()

    @classmethod
    def get_by_user(cls, user: User) -> list[UserAnswer]:
        with Session(engine) as db:
            user_entity = UserOps.get_by_username(db, user.username)
            ret = [cls.entity_to_model(answer, user)
                   for answer in user_entity.answers]
            return ret
