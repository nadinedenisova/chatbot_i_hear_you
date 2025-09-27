import uuid
from datetime import datetime, timezone

from sqlalchemy import text, func, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from src.db.postgres import Base
from src.models.users import User


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text('gen_random_uuid()'),
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id')
    )

    user: Mapped[User] = relationship(
        back_populates='questions'
    )

    text: Mapped[str] = mapped_column(
        String(255)
    )

    admin_answer: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f'<Question(id={self.id}'
