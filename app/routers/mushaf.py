"""Mushaf pages, images, fonts, and coordinates router."""

from fastapi import APIRouter, HTTPException, Query

from app.services.quran_images import (
    MUSHAF_VERSIONS,
    page_url,
    line_url,
    font_url,
    get_page_coordinates,
    get_line_coordinates,
    get_line_forayah,
)

router = APIRouter()


@router.get("/versions")
def list_versions():
    """List available mushaf visual styles."""
    return {
        "versions": [
            {
                "id": vid,
                "name": v["name"],
                "format": v["format"],
                "description": v["description"],
            }
            for vid, v in MUSHAF_VERSIONS.items()
        ]
    }


@router.get("/{version}/page/{page}")
def get_page(version: str, page: int):
    """Get mushaf page image URL and coordinates."""
    if page < 1 or page > 604:
        raise HTTPException(status_code=400, detail="Page must be between 1 and 604")

    try:
        image_url = page_url(version, page)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    coords = get_page_coordinates(page)

    return {
        "version": version,
        "page": page,
        "image_url": image_url,
        "coordinates": coords,
    }


@router.get("/page/{page}/lines")
def get_page_lines(page: int):
    """Get all lines on a mushaf page with their ayah mappings."""
    if page < 1 or page > 604:
        raise HTTPException(status_code=400, detail="Page must be between 1 and 604")

    coords = get_line_coordinates(page)
    if not coords:
        return {"page": page, "lines": {}}

    lines = coords.get("lines", {})
    result = {}
    for line_num, line_data in lines.items():
        result[line_num] = {
            "image_url": line_url(page, int(line_num)),
            **line_data,
        }

    return {
        "page": page,
        "surah_start": coords.get("surah_start"),
        "surah_end": coords.get("surah_end"),
        "ayah_start": coords.get("ayah_start"),
        "ayah_end": coords.get("ayah_end"),
        "lines": result,
    }


@router.get("/page/{page}/line/{line}")
def get_line(page: int, line: int):
    """Get a specific line image URL and ayah mapping."""
    if page < 1 or page > 604:
        raise HTTPException(status_code=400, detail="Page must be between 1 and 604")
    if line < 1 or line > 15:
        raise HTTPException(status_code=400, detail="Line must be between 1 and 15")

    coords = get_line_coordinates(page)
    lines = coords.get("lines", {}) if coords else {}
    line_data = lines.get(str(line))

    if not line_data:
        raise HTTPException(status_code=404, detail="Line not found")

    return {
        "page": page,
        "line": line,
        "image_url": line_url(page, line),
        **line_data,
    }


@router.get("/font/{page}")
def get_font(page: int):
    """Get WOFF2 font URL for a mushaf page."""
    if page < 1 or page > 604:
        raise HTTPException(status_code=400, detail="Page must be between 1 and 604")

    return {
        "page": page,
        "font_url": font_url(page),
        "format": "woff2",
        "description": "Quran Bihari Calligraphy v2 — renders full page as scalable web font",
    }


@router.get("/ayah-location/{surah}/{ayah}")
def get_ayah_location(surah: int, ayah: int):
    """Find which page and line an ayah is on."""
    if surah < 1 or surah > 114:
        raise HTTPException(status_code=400, detail="Surah must be between 1 and 114")

    from app.services.data_loader import get_store
    store = get_store()

    surah_data = next((s for s in store.quran_surahs if s["number"] == surah), None)
    if not surah_data:
        raise HTTPException(status_code=404, detail="Surah not found")

    ayah_count = surah_data.get("ayah_count", 0)
    if ayah < 1 or ayah > ayah_count:
        raise HTTPException(status_code=400, detail=f"Ayah must be between 1 and {ayah_count}")

    for page_num in range(1, 605):
        line_coords = get_line_coordinates(page_num)
        if not line_coords:
            continue
        lines = line_coords.get("lines", {})
        for line_num, line_data in lines.items():
            if line_data.get("surah") == surah:
                if line_data.get("ayah_start") <= ayah <= line_data.get("ayah_end", ayah):
                    return {
                        "surah": surah,
                        "ayah": ayah,
                        "page": page_num,
                        "line": int(line_num),
                        "line_image_url": line_url(page_num, int(line_num)),
                        "surah_name_ar": line_data.get("surah_name_ar"),
                        "surah_name_en": line_data.get("surah_name_en"),
                    }

    return {
        "surah": surah,
        "ayah": ayah,
        "page": None,
        "line": None,
        "note": "Coordinates not available for this ayah",
    }
