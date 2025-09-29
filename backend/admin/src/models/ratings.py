import uuid
from datetime import datetime, timezone

from sqlalchemy import text, func, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from src.db.postgres import Base


class UserMenuNode(Base):
    __tablename__ = "user_menu_node"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        index=True,
    )

    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("user.id"))

    user: Mapped["User"] = relationship("User", back_populates="ratings")

    menu_id: Mapped[uuid.UUID]

    post_rating: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<UserMenuNode(user_id={self.user_id}"
