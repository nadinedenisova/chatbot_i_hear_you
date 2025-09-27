import uuid
from datetime import datetime, timezone

from sqlalchemy import text, func, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from src.db.postgres import Base


class Content(Base):
    __tablename__ = 'contents'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text('gen_random_uuid()'),
        index=True,
    )

    # TODO
    # menu_id: Mapped[uuid.UUID]

    type: Mapped[int]

    server_path: Mapped[str]

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
