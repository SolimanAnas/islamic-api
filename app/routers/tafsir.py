import sqlite3
from pathlib import Path
from fastapi import APIRouter, Query, HTTPException

from app.config import get_settings

router = APIRouter()
settings = get_settings()

TAFSIR_DB_MAP = {
    "qurtubi": "tafsir-qurtobi.db",
    "ibn-kathir": "tafsir-ibn-kathir.db",
    "baghawi": "tafsir-baghawi.db",
    "saadi": "tafsir-saadi.db",
}


def _get_db(book: str):
    db_file = TAFSIR_DB_MAP.get(book)
    if not db_file:
        return None
    db_path = Path(settings.TAFSIR_DIR) / db_file
    if not db_path.exists():
        return None
    return sqlite3.connect(str(db_path))


@router.get("/books", summary="List available tafsir books")
def list_tafsir_books():
    available = []
    for key, db_file in TAFSIR_DB_MAP.items():
        db_path = Path(settings.TAFSIR_DIR) / db_file
        available.append({
            "id": key,
            "name": db_file.replace(".db", "").replace("tafsir-", "").replace("-", " ").title(),
            "available": db_path.exists(),
        })
    return {"success": True, "data": available}


@router.get("/{book}/{surah}", summary="Get tafsir for a surah")
def get_tafsir_surah(book: str, surah: int):
    conn = _get_db(book)
    if not conn:
        raise HTTPException(status_code=404, detail=f"Tafsir '{book}' not available")

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tafsir WHERE surah = ? ORDER BY ayah",
            (surah,),
        )
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        data = [dict(zip(cols, row)) for row in rows]
        return {"success": True, "data": data, "count": len(data)}
    finally:
        conn.close()


@router.get("/{book}/{surah}/{ayah}", summary="Get tafsir for a specific ayah")
def get_tafsir_ayah(book: str, surah: int, ayah: int):
    conn = _get_db(book)
    if not conn:
        raise HTTPException(status_code=404, detail=f"Tafsir '{book}' not available")

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tafsir WHERE surah = ? AND ayah = ?",
            (surah, ayah),
        )
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        data = [dict(zip(cols, row)) for row in rows]
        if not data:
            raise HTTPException(status_code=404, detail="Tafsir not found for this ayah")
        return {"success": True, "data": data[0]}
    finally:
        conn.close()


@router.get("/{book}/search", summary="Search within a tafsir book")
def search_tafsir(
    book: str,
    q: str = Query(..., min_length=2, description="Search query"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    conn = _get_db(book)
    if not conn:
        raise HTTPException(status_code=404, detail=f"Tafsir '{book}' not available")

    try:
        cursor = conn.cursor()
        offset = (page - 1) * per_page
        cursor.execute(
            "SELECT COUNT(*) FROM tafsir WHERE text LIKE ?",
            (f"%{q}%",),
        )
        total = cursor.fetchone()[0]
        cursor.execute(
            "SELECT * FROM tafsir WHERE text LIKE ? LIMIT ? OFFSET ?",
            (f"%{q}%", per_page, offset),
        )
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        data = [dict(zip(cols, row)) for row in rows]
        return {
            "success": True,
            "data": data,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": max(1, (total + per_page - 1) // per_page),
            },
        }
    finally:
        conn.close()
