from fastapi import Query
from typing import Optional

class ArticleFilters:
    def __init__(
        self,
        search: Optional[str] = Query(None, description="Filter by title"),
        category_id: Optional[int] = Query(None, description="Filter by category id"),
    ):
        self.search = search
        self.category_id = category_id