import uuid
from datetime import datetime, timezone

from sqlalchemy import func, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from src.db.postgres import Base
from src.models.users import User


class UserMenuNode(Base):
    __tablename__ = 'user_menu_node'

    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id')
    )

    user: Mapped[User] = relationship(
        back_populates='ratings'
    )

    menu_id: Mapped[uuid.UUID]

    post_rating: Mapped[int]

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
        return f'<UserMenuNode(user_id={self.user_id}'
