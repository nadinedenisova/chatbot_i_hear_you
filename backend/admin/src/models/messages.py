import uuid

from sqlalchemy import text, String
from sqlalchemy.orm import mapped_column, Mapped
from src.db.postgres import Base


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text('gen_random_uuid()'),
        index=True,
    )

    detail: Mapped[str] = mapped_column(
        String(255)
    )
