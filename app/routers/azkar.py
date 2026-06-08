from fastapi import APIRouter, Query, HTTPException

from app.services.data_loader import get_store
from app.utils.pagination import paginate, search_items

router = APIRouter()


@router.get("/hisn/chapters", summary="List all Hisn Muslim chapters")
def list_hisn_chapters():
    store = get_store()
    return {
        "success": True,
        "data": [
            {
                "id": ch.get("id", ""),
                "title": ch.get("title", ""),
                "title_en": ch.get("title_en", ""),
                "items_count": len(ch.get("items", [])),
            }
            for ch in store.hisn_chapters
        ],
    }


@router.get("/hisn/{chapter_id}", summary="Get a Hisn Muslim chapter")
def get_hisn_chapter(chapter_id: str):
    store = get_store()
    for ch in store.hisn_chapters:
        if ch.get("id") == chapter_id:
            return {"success": True, "data": ch}
    raise HTTPException(status_code=404, detail="Chapter not found")


@router.get("/morning", summary="Morning adhkar (أذكار الصباح)")
def get_morning_adhkar():
    store = get_store()
    return {"success": True, "data": store.azkar_morning, "count": len(store.azkar_morning)}


@router.get("/evening", summary="Evening adhkar (أذكار المساء)")
def get_evening_adhkar():
    store = get_store()
    return {"success": True, "data": store.azkar_evening, "count": len(store.azkar_evening)}


@router.get("/sleeping", summary="Sleeping adhkar (أذكار النوم)")
def get_sleeping_adhkar():
    store = get_store()
    return {"success": True, "data": store.azkar_sleeping, "count": len(store.azkar_sleeping)}


@router.get("/post-salah", summary="Post-salah adhkar (أذكار بعد الصلاة)")
def get_post_salah_adhkar():
    store = get_store()
    return {"success": True, "data": store.salah, "count": len(store.salah)}


@router.get("/search", summary="Search across all adhkar")
def search_azkar(
    q: str = Query(..., min_length=2, description="Search query"),
    lang: str = Query("ar", description="Language: ar or en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    store = get_store()
    all_items = []
    all_items.extend(store.azkar_morning)
    all_items.extend(store.azkar_evening)
    all_items.extend(store.azkar_sleeping)
    all_items.extend(store.salah)

    for ch in store.hisn_chapters:
        all_items.extend(ch.get("items", []))

    fields = ["arabic", "ar", "english", "en", "transliteration"]
    results = search_items(all_items, q, fields)
    data, meta = paginate(results, page, per_page)
    return {"success": True, "data": data, "meta": meta}
