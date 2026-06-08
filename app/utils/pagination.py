import math
from fastapi import Query


def paginate(items: list, page: int = 1, per_page: int = 20) -> tuple[list, dict]:
    total = len(items)
    total_pages = max(1, math.ceil(total / per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
    }


def search_items(items: list, query: str, fields: list[str]) -> list:
    q = query.lower()
    return [
        item for item in items
        if any(q in str(item.get(f, "")).lower() for f in fields)
    ]


def pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
):
    return page, per_page
