from uuid import UUID
from datetime import datetime  # Изменено с date на datetime

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
    created_at: datetime = Field(..., description="Дата и время создания")  # Изменено
    updated_at: datetime = Field(
        ..., description="Дата и время последнего обновления"
    )  # Изменено


class QuestionsListOut(BaseModel):
    items: list[QuestionOut] = Field(..., description="Список вопросов")


class ContentOut(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор контента")
    menu_id: UUID = Field(
        ..., description="Идентификатор меню, к которому относится контент"
    )
    type: int = Field(..., description="Тип контента (числовой код)")
    server_path: str = Field(..., description="Серверный путь до контента")
    created_at: datetime = Field(..., description="Дата и время создания")  # Изменено
    updated_at: datetime = Field(
        ..., description="Дата и время последнего обновления"
    )  # Изменено


class MenuNodeOut(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор узла меню")
    parent_id: UUID | None = Field(
        None, description="Идентификатор родительского узла (если есть)"
    )
    name: str = Field(..., description="Имя узла меню")
    text: str | None = Field(None, description="Текстовое наполнение узла")
    subscription_type: str | None = Field(None, description="Тип подписки (если есть)")
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


class QuestionAnswer(BaseModel):
    admin_answer: str = Field(..., description="Текст вопроса")


class UserCreate(BaseModel):
    id: str = Field(..., description="Уникальный идентификатор пользователя")
    phone_number: str = Field(..., description="Номер телефона пользователя")


class UserOut(UserCreate):
    created_at: datetime = Field(
        ..., description="Дата и время создания пользователя"
    )  # Изменено
    updated_at: datetime = Field(
        ..., description="Дата и время последнего обновления пользователя"
    )  # Изменено


class UsersListOut(BaseModel):
    items: list[UserOut] = Field(..., description="Список пользователей")


class HistoryCreate(BaseModel):
    menu_id: UUID | None = Field(
        None, description="Идентификатор меню (необязательный)"
    )
    action_date: datetime = Field(..., description="Дата и время действия")  # Изменено


class HistoryOut(HistoryCreate):
    user_id: str = Field(..., description="Идентификатор пользователя")
    action_id: UUID = Field(..., description="Идентификатор действия")
    created_at: datetime = Field(
        ..., description="Дата и время создания записи истории"
    )  # Изменено


class HistoryListOut(BaseModel):
    items: list[HistoryOut] = Field(..., description="Список действий")


class RatingCreate(BaseModel):
    user_id: str = Field(..., description="Идентификатор пользователя")
    is_useful: bool = Field(..., description="true - Полезно, false - Не очень")


class RatingSummaryOut(BaseModel):
    menu_id: UUID
    useful_count: int = Field(..., description="Количество оценок 'Полезно'")
    not_useful_count: int = Field(..., description="Количество оценок 'Не очень'")

    class Config:
        from_attributes = True


AllMenuNodeOut.model_rebuild()
