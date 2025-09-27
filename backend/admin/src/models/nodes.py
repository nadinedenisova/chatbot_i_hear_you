import uuid

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, relationship, Mapped
from src.db.postgres import Base
from src.models.contents import Content


class MenuNode(Base):
    __tablename__ = 'menu_nodes'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text('gen_random_uuid()'),
        index=True,
    )

    parent_id: Mapped[uuid.UUID | None]

    name: Mapped[str]

    text: Mapped[str | None]

    subscription_type: Mapped[str | None]

    content: Mapped[list[Content]] = relationship(
        back_populates='menu_node'
    )
