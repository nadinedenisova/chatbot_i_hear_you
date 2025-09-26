from fastapi import Query

class PaginatedParams:
    def __init__(
        self,
        page_size: int = Query(50, ge=1, le=100, description="Количество записей на странице"),
        page_number: int = Query(1, ge=1, description="Номер страницы"),
    ):
        self.page_size = page_size
        self.page_number = page_number