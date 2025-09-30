import uuid
from datetime import datetime, timezone

from sqlalchemy import text, func, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from db.postgres import Base


class Question(Base):
    __tablename__ = "question"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship("User", back_populates="questions")

    text: Mapped[str]

    admin_answer: Mapped[str | None]

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
        return f"<Question(id={self.id}"
