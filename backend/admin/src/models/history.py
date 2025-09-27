import uuid
from datetime import datetime, timezone

from sqlalchemy import text, func, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from src.db.postgres import Base
from src.models.users import User


class History(Base):
    __tablename__ = 'history'

    action_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text('gen_random_uuid()'),
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey('users.id')
    )

    user: Mapped[User] = relationship(
        back_populates='history'
    )

    menu_id: Mapped[uuid.UUID | None]

    action_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f'<History(id={self.id}'
