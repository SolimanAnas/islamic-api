from fastapi import APIRouter, Query, HTTPException

from app.services.data_loader import get_store
from app.utils.pagination import paginate, search_items

router = APIRouter()


@router.get("/books", summary="List all dua books")
def list_dua_books():
    store = get_store()
    return {
        "success": True,
        "data": [
            {"id": book["id"], "title": book["title"], "items_count": len(book.get("items", []))}
            for book in store.dua_books.values()
        ],
    }


@router.get("/{book_id}", summary="Get a dua book")
def get_dua_book(book_id: str):
    store = get_store()
    book = store.dua_books.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book '{book_id}' not found")
    return {"success": True, "data": book}


@router.get("/search", summary="Search across all duas")
def search_duas(
    q: str = Query(..., min_length=2, description="Search query"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    store = get_store()
    all_items = []
    for book in store.dua_books.values():
        all_items.extend(book.get("items", []))

    results = search_items(all_items, q, ["arabic", "ar", "title"])
    data, meta = paginate(results, page, per_page)
    return {"success": True, "data": data, "meta": meta}
