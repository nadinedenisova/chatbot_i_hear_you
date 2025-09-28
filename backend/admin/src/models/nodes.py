import uuid

from sqlalchemy import text, String
from sqlalchemy.orm import mapped_column, relationship, Mapped
from db.postgres import Base


class MenuNode(Base):
    __tablename__ = "menu_node"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        index=True,
    )

    parent_id: Mapped[uuid.UUID | None]

    name: Mapped[str] = mapped_column(String(255))

    text: Mapped[str | None]

    subscription_type: Mapped[str | None] = mapped_column(String(255))

    content: Mapped[list] = relationship("Content", back_populates="menu_node")

    def __repr__(self):
        return f"<MenuNode(id={self.id}"
