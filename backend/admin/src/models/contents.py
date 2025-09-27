import uuid
from datetime import datetime, timezone

from sqlalchemy import text, func, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from src.db.postgres import Base
from src.models.nodes import MenuNode


class Content(Base):
    __tablename__ = 'contents'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text('gen_random_uuid()'),
        index=True,
    )

    menu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('menu_nodes.id')
    )

    menu_node: Mapped[MenuNode] = relationship(
        back_populates='content'
    )

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
