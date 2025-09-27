import uuid

from sqlalchemy import text, String
from sqlalchemy.orm import mapped_column, relationship, Mapped
from src.db.postgres import Base
from src.models.questions import Question
from src.models.history import History
from src.models.ratings import Rating


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text('gen_random_uuid()'),
        index=True,
    )

    phone_number: Mapped[str] = mapped_column(
        String(30)
    )

    questions: Mapped[list[Question]] = relationship(
        back_populates='user'
    )

    history: Mapped[list[History]] = relationship(
        back_populates='user'
    )

    ratings: Mapped[list[Rating]] = relationship(
        back_populates='user'
    )

    def __repr__(self):
        return f'<User(id={self.id}'
