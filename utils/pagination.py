from typing import Tuple
from sqlalchemy.orm import Query


def paginate_query(query: Query, page: int, size: int) -> Tuple[int, int, int]:
    total = query.count()
    pages = (total + size - 1) // size
    offset = (page - 1) * size
    return total, pages, offset
