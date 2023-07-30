from sqlalchemy import Column, MetaData, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import String
from database.mixins import TimestampMixin


_metadata = MetaData()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    metadata = _metadata


user_answer_table = Table(
    'user_answer',
    Base.metadata,
    Column('user_id', ForeignKey('user.id')),
    Column('answer_id', ForeignKey('answer.id'))
)


class UserEntity(Base, TimestampMixin):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String(64), unique=True)
    first_name: Mapped[str] = mapped_column(String(64), default='')
    last_name: Mapped[str] = mapped_column(String(64), default='')

    answers: Mapped[list['AnswerEntity']] = relationship(
        secondary=user_answer_table, back_populates='users')



class QuestionEntity(Base, TimestampMixin):
    __tablename__ = 'question'

    title: Mapped[str] = mapped_column(String(64))
    answers: Mapped[list['AnswerEntity']] = relationship(
        back_populates='question')


class AnswerEntity(Base):
    __tablename__ = 'answer'

    question: Mapped[QuestionEntity] = relationship(back_populates='answers')
    question_id: Mapped[int] = mapped_column(
        ForeignKey(QuestionEntity.id, ondelete='CASCADE'))
    text: Mapped[str] = mapped_column(String(64))
    users: Mapped[list['UserEntity']] = relationship(
        secondary=user_answer_table, back_populates='answers')
