from uuid import UUID
from fastapi import APIRouter, Depends, Query
from redis.asyncio import Redis
from src.db.redis import get_redis
from src.schemas.entity import (
    ContentCreate,
    MenuNodeOut,
    MenuNodeCreate,
    MenuNodeUpdate,
    Message,
    RatingCreate,
    RatingSummaryOut,
    RatingListOut,
    AllMenuNodeOut,
)
from src.services.menu_service import MenuService, get_menu_service
from src.utils.pagination import PaginatedParams


router = APIRouter()


@router.get(
    "/", summary="Получить всё дерево меню навигации", response_model=AllMenuNodeOut
)
async def get_full_menu(
    menu_service: MenuService = Depends(get_menu_service),
    redis: Redis = Depends(get_redis)
):
    full_menu_key = 'full_menu'
    full_menu = await redis.get(full_menu_key)

    if full_menu:
        return AllMenuNodeOut.model_validate_json(full_menu)

    full_menu = await menu_service.get_full_menu()

    # закешируем на 1 час
    await redis.setex(full_menu_key, 3600, full_menu.model_dump_json())

    return full_menu


@router.get(
    "/search-by-name",
    summary="Получить узел меню по названию",
    response_model=MenuNodeOut,
)
async def get_menu_node_by_name(
    name: str = Query(..., title="Название узла", max_length=100),
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.get_menu_node_by_name(name)


@router.get(
    "/root", summary="Получить корень узла меню навигации", response_model=MenuNodeOut
)
async def get_menu_root(menu_service: MenuService = Depends(get_menu_service)):
    return await menu_service.get_menu_root()


@router.post("/add", summary="Добавить узел меню навигации", response_model=Message)
async def add_menu_node(
    node_data: MenuNodeCreate, menu_service: MenuService = Depends(get_menu_service)
):
    return await menu_service.add_menu_node(node_data)


@router.get(
    "/{menu_id}", summary="Получить узел меню по id", response_model=MenuNodeOut
)
async def get_menu_node(
    menu_id: UUID, menu_service: MenuService = Depends(get_menu_service)
):
    return await menu_service.get_menu_node_by_id(menu_id)


@router.put("/{menu_id}", summary="Обновить узел меню по id", response_model=Message)
async def update_menu_node(
    menu_id: UUID,
    node_data: MenuNodeUpdate,
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.update_menu_node(menu_id, node_data)


@router.delete("/{menu_id}", summary="Удалить узел меню по id", response_model=Message)
async def delete_menu_node(
    menu_id: UUID, menu_service: MenuService = Depends(get_menu_service)
):
    return await menu_service.delete_menu_node(menu_id)


@router.post(
    "/{menu_id}/content/add",
    summary="Добавить контент к узлу меню",
    response_model=Message,
)
async def add_menu_content(
    menu_id: UUID,
    content_data: ContentCreate,
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.add_menu_content(menu_id, content_data)


@router.put(
    "/{menu_id}/content/change/{content_id}",
    summary="Обновить контент",
    response_model=Message,
)
async def update_menu_content(
    menu_id: UUID,
    content_id: UUID,
    content_data: ContentCreate,
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.update_menu_content(content_id, content_data)


@router.delete(
    "/{menu_id}/content/delete/{content_id}",
    summary="Удалить контент",
    response_model=Message,
)
async def delete_menu_content(
    menu_id: UUID,
    content_id: UUID,
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.delete_menu_content(content_id)


@router.get(
    "/{menu_id}/rate", summary="Получить рейтинг узла меню", response_model=RatingSummaryOut
)
async def get_menu_node_rate(
    menu_id: UUID, menu_service: MenuService = Depends(get_menu_service)
):
    return await menu_service.get_menu_node_rate(menu_id)


@router.post("/{menu_id}/rate", summary="Оценить узел меню", response_model=Message)
async def rate_menu_node(
    menu_id: UUID,
    rating_data: RatingCreate,
    menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.rate_menu_node(menu_id, rating_data)


@router.get(
    "/{menu_id}/rates-all",
    summary="Получить все оценки пользователей для узла меню",
    response_model=RatingListOut
)
async def get_menu_ratings_all(
    menu_id: UUID,
    pagination: PaginatedParams = Depends(),
    menu_service: MenuService = Depends(get_menu_service)
):
    return await menu_service.get_menu_ratings_all(menu_id, pagination)
