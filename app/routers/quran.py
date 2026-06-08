from fastapi import APIRouter, Query, HTTPException

from app.services.data_loader import get_store
from app.utils.pagination import paginate, search_items, pagination_params

router = APIRouter()


@router.get("/surahs", summary="List all 114 surahs")
def list_surahs():
    store = get_store()
    return {
        "success": True,
        "data": [
            {
                "number": s["number"],
                "name_ar": s["name_ar"],
                "name_en": s["name_en"],
                "ayah_count": s["ayah_count"],
            }
            for s in store.quran_surahs
        ],
    }


@router.get("/surah/{surah_id}", summary="Get surah with all ayahs")
def get_surah(surah_id: int):
    store = get_store()
    if surah_id < 1 or surah_id > 114:
        raise HTTPException(status_code=404, detail="Surah not found")
    surah = next((s for s in store.quran_surahs if s["number"] == surah_id), None)
    if not surah:
        raise HTTPException(status_code=404, detail="Surah not found")
    return {"success": True, "data": surah}


@router.get("/ayah/{surah_id}/{ayah_id}", summary="Get a single ayah")
def get_ayah(surah_id: int, ayah_id: int):
    store = get_store()
    for a in store.quran_ayahs:
        if a["surah"] == surah_id and a["ayah"] == ayah_id:
            return {"success": True, "data": a}
    raise HTTPException(status_code=404, detail="Ayah not found")


@router.get("/juz/{juz_id}", summary="Get ayahs in a juz")
def get_juz(juz_id: int):
    store = get_store()
    if juz_id < 1 or juz_id > 30:
        raise HTTPException(status_code=400, detail="Juz must be 1-30")

    juz_boundaries = {
        1: (1, 1), 2: (2, 142), 3: (2, 253), 4: (3, 92), 5: (4, 24),
        6: (4, 148), 7: (5, 82), 8: (6, 111), 9: (7, 88), 10: (8, 41),
        11: (9, 93), 12: (11, 6), 13: (12, 53), 14: (15, 1), 15: (17, 1),
        16: (18, 75), 17: (21, 1), 18: (23, 1), 19: (25, 1), 20: (27, 56),
        21: (29, 1), 22: (33, 1), 23: (35, 1), 24: (38, 1), 25: (41, 1),
        26: (46, 1), 27: (51, 1), 28: (58, 1), 29: (67, 1), 30: (78, 1),
    }

    start_surah, start_ayah = juz_boundaries.get(juz_id, (1, 1))
    if juz_id == 30:
        end_surah, end_ayah = 114, 6
    else:
        end_surah, end_ayah = juz_boundaries.get(juz_id + 1, (114, 6))
        if end_ayah > 1:
            end_ayah -= 1
        else:
            end_surah -= 1
            end_ayah = 9999

    ayahs = []
    for a in store.quran_ayahs:
        s, ay = a["surah"], a["ayah"]
        if s < start_surah or (s == start_surah and ay < start_ayah):
            continue
        if s > end_surah or (s == end_surah and ay > end_ayah):
            break
        ayahs.append(a)

    return {"success": True, "data": {"juz": juz_id, "ayah_count": len(ayahs), "ayahs": ayahs}}


@router.get("/page/{page_number}", summary="Get ayahs on a mushaf page")
def get_page(page_number: int):
    store = get_store()
    if page_number < 1 or page_number > 604:
        raise HTTPException(status_code=400, detail="Page must be 1-604")
    ayahs = [a for a in store.quran_ayahs if a.get("page") == page_number]
    return {"success": True, "data": {"page": page_number, "ayah_count": len(ayahs), "ayahs": ayahs}}


@router.get("/search", summary="Search Quran text")
def search_quran(
    q: str = Query(..., min_length=2, description="Search query"),
    lang: str = Query("ar", description="Language: ar or en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    store = get_store()
    field = "text_clean" if lang == "ar" else "text_clean"
    results = search_items(store.quran_ayahs, q, [field])
    data, meta = paginate(results, page, per_page)
    return {"success": True, "data": data, "meta": meta}
