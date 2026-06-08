from fastapi import APIRouter, Query

from app.services.data_loader import get_store
from app.utils.pagination import paginate

router = APIRouter()


@router.get("/stations", summary="List Quran radio stations")
def list_radio_stations(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
):
    store = get_store()
    data, meta = paginate(store.radio_stations, page, per_page)
    return {"success": True, "data": data, "meta": meta}


@router.get("/reciters", summary="List Quran reciters")
def list_reciters():
    store = get_store()
    return {"success": True, "data": store.reciters, "count": len(store.reciters)}
