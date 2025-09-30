from redis.asyncio import Redis

from src.core.settings import settings


_redis: Redis | None = None


def get_redis(refresh: bool = False) -> Redis:
    """
    Возвращает экземпляр соединения с Redis.

    Args
    ----
    refresh
        Индикатор необходимости обновить соединение.
    """

    global _redis

    if _redis is None or refresh:
        _redis = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
        )

    return _redis
