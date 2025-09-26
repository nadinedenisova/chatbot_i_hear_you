from uuid import UUID
from datetime import date

from pydantic import BaseModel, Field


class Message(BaseModel):
    detail: str = Field(default="", description="Сообщение об ошибке или информация")


class QuestionOut(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор вопроса")
    user_id: str = Field(
        ..., description="Идентификатор пользователя, задавшего вопрос"
    )
    text: str = Field(..., description="Текст вопроса")
    admin_answer: str | None = Field(
        None, description="Ответ администратора (может отсутствовать)"
    )
    created_at: date = Field(..., description="Дата создания")
    updated_at: date = Field(..., description="Дата последнего обновления")


class QuestionsListOut(BaseModel):
    items: list[QuestionOut] = Field(..., description="Список вопросов")


class ContentOut(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор контента")
    menu_id: UUID = Field(
        ..., description="Идентификатор меню, к которому относится контент"
    )
    type: int = Field(..., description="Тип контента (числовой код)")
    server_path: str = Field(..., description="Серверный путь до контента")
    created_at: date = Field(..., description="Дата создания")
    updated_at: date = Field(..., description="Дата последнего обновления")


class MenuNodeOut(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор узла меню")
    parent_id: UUID | None = Field(
        None, description="Идентификатор родительского узла (если есть)"
    )
    name: str = Field(..., description="Имя узла меню")
    text: str | None = Field(None, description="Текстовое наполнение узла")
    subscription_type: str | None = Field(
        None, description="Тип подписки (если есть)"
    )
    content: list[ContentOut] = Field(
        ..., description="Список контента, привязанного к узлу"
    )
    children_names: list[str] = Field(..., description="Имена дочерних узлов меню")


class MenuNodeCreate(BaseModel):
    parent_id: UUID | None = Field(
        None, description="Идентификатор родительского узла (необязательный)"
    )
    name: str = Field(..., description="Имя нового узла")
    text: str | None = Field(None, description="Текст узла (необязательный)")
    subscription_type: str | None = Field(
        None, description="Тип подписки (необязательный)"
    )


class MenuNodeUpdate(MenuNodeCreate):
    """То же, что MenuNodeCreate, используется для обновления."""

    pass


class ContentCreate(BaseModel):
    menu_id: UUID = Field(
        ..., description="Идентификатор меню, к которому привязывается контент"
    )
    type: int = Field(..., description="Тип контента (числовой код)")
    server_path: str = Field(
        ..., description="Серверный путь для загружаемого контента"
    )

class AllMenuNodeOut(MenuNodeOut):
    children: list["AllMenuNodeOut"] = Field(..., description="Дочерние узлы меню")

class QuestionCreate(BaseModel):
    user_id: str = Field(
        ..., description="Идентификатор пользователя, задающего вопрос"
    )
    text: str = Field(..., description="Текст вопроса")


class UserCreate(BaseModel):
    id: str = Field(..., description="Уникальный идентификатор пользователя")
    phone_number: str = Field(..., description="Номер телефона пользователя")


class UserOut(UserCreate):
    created_at: date = Field(..., description="Дата создания пользователя")
    updated_at: date = Field(..., description="Дата последнего обновления пользователя")


class UsersListOut(BaseModel):
    items: list[UserOut] = Field(..., description="Список пользователей")


class HistoryCreate(BaseModel):
    user_id: str = Field(..., description="Идентификатор пользователя")
    menu_id: UUID | None = Field(
        None, description="Идентификатор меню (необязательный)"
    )
    action_date: date = Field(..., description="Дата действия")


class HistoryOut(HistoryCreate):
    action_id: UUID = Field(..., description="Идентификатор действия")
    created_at: date = Field(..., description="Дата создания записи истории")


class RatingCreate(BaseModel):
    user_id: str = Field(..., description="Идентификатор пользователя")
    node_rating: int = Field(
        ..., ge=1, le=5, description="Оценка (например, от 1 до 5)"
    )


class RatingOut(RatingCreate):
    menu_id: UUID = Field(
        ..., description="Идентификатор меню/узла, к которому привязана оценка"
    )
    created_at: date = Field(..., description="Дата создания оценки")
    updated_at: date = Field(..., description="Дата обновления оценки")

AllMenuNodeOut.model_rebuild()
