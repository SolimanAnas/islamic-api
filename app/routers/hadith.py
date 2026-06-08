from fastapi import APIRouter, Query, HTTPException

from app.services.data_loader import get_store
from app.utils.pagination import paginate, search_items, pagination_params

router = APIRouter()


@router.get("/collections", summary="List all hadith collections")
def list_collections():
    store = get_store()
    return {
        "success": True,
        "data": [
            {
                "id": c["id"],
                "name_ar": c["name_ar"],
                "name_en": c["name_en"],
                "total_hadith": c["total_hadith"],
                "sections_count": len(c["sections"]),
            }
            for c in store.hadith_collections.values()
        ],
    }


@router.get("/{collection}", summary="Get hadith collection with chapters")
def get_collection(
    collection: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    store = get_store()
    col = store.hadith_collections.get(collection)
    if not col:
        raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")

    hadiths = col["hadiths"]
    data, meta = paginate(hadiths, page, per_page)
    return {
        "success": True,
        "data": {
            "id": col["id"],
            "name_ar": col["name_ar"],
            "name_en": col["name_en"],
            "total_hadith": col["total_hadith"],
            "sections": col["sections"],
            "hadiths": data,
        },
        "meta": meta,
    }


@router.get("/{collection}/{hadith_id}", summary="Get a single hadith")
def get_hadith(collection: str, hadith_id: int):
    store = get_store()
    col = store.hadith_collections.get(collection)
    if not col:
        raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")

    for h in col["hadiths"]:
        if h.get("hadithNumber") == hadith_id or h.get("id") == hadith_id:
            return {"success": True, "data": h}

    raise HTTPException(status_code=404, detail="Hadith not found")


@router.get("/{collection}/sections", summary="List sections in a collection")
def list_sections(collection: str):
    store = get_store()
    col = store.hadith_collections.get(collection)
    if not col:
        raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    return {"success": True, "data": col["sections"]}


@router.get("/search", summary="Search across all hadith collections")
def search_hadith(
    q: str = Query(..., min_length=2, description="Search query"),
    collection: str | None = Query(None, description="Limit to specific collection"),
    lang: str = Query("en", description="Language: ar or en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    store = get_store()
    fields = ["englishText", "arabicText"] if lang == "en" else ["arabicText"]
    all_hadith = []

    if collection:
        col = store.hadith_collections.get(collection)
        if col:
            all_hadith = col["hadiths"]
    else:
        for col in store.hadith_collections.values():
            all_hadith.extend(col["hadiths"])

    results = search_items(all_hadith, q, fields)
    data, meta = paginate(results, page, per_page)
    return {"success": True, "data": data, "meta": meta}


@router.get("/random/{collection}", summary="Get random hadith from collection")
def random_hadith(collection: str):
    import random
    store = get_store()
    col = store.hadith_collections.get(collection)
    if not col:
        raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    h = random.choice(col["hadiths"])
    return {"success": True, "data": h}
